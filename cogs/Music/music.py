import asyncio
import functools
import itertools
import math
import random

import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands
from discord.ext.commands import Cog
from .utils.Song import Song
from .utils.SongQueue import SongQueue
from .utils.VoiceState import VoiceState
from .utils.YTDLSource import YTDLSource


class Music(Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('이 명령은 DM 채널에서 사용할 수 없습니다.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('{} 오류가 발생했습니다.'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """음성 채널에 가입합니다."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon', aliases=['call'])
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """봇을 음성 채널로 전송합니다.
        채널이 지정되지 않은 경우 채널에 연결됩니다.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError('음성 채널에 연결되어 있지 않거나 가입할 채널을 지정하지 않았습니다.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect', 'off'])
    async def _leave(self, ctx: commands.Context):

        if not ctx.voice_state.voice:
            return await ctx.send('어떤 음성 채널에도 연결되지 않았습니다.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume', aliases=['vol'])
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """플레이어의 볼륨을 설정합니다."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('현재 재생 중인 것은 없습니다.')

        if 0 > volume > 100:
            return await ctx.send('볼륨은 0에서 100 사이여야 합니다.')

        ctx.voice_state.volume = volume / 100
        await ctx.send('플레이어 볼륨이 {}%로 설정되었습니다.'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        """현재 재생 중인 노래를 표시합니다."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause', aliases=['일시중지'])
    async def _pause(self, ctx: commands.Context):
        """현재 재생 중인 노래를 일시 중지합니다."""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='resume', aliases=['res'])
    async def _resume(self, ctx: commands.Context):
        """현재 일시 중지된 노래를 다시 시작합니다."""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='stop')
    async def _stop(self, ctx: commands.Context):
        """노래 재생을 중지하고 재생목록을 지웁니다."""

        ctx.voice_state.songs.clear()

        if not ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name='skip', aliases=['스킵', 'sp'])
    async def _skip(self, ctx: commands.Context):
        """한 곡 건너뛰는 걸로 투표하세요. 요청자는 자동으로 건너뛸 수 있습니다.
        건너뛰기 위해서는 3개의 건너뛰기 표가 필요합니다.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('지금은 음악을 재생중이 아닙니다.')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('현재 **{}/3** 위치에서 생략 투표가 추가되었습니다.'.format(total_votes))

        else:
            await ctx.send('이 노래를 건너뛰기로 이미 명령을 실행하였습니다.')

    @commands.command(name='queue', aliases=['재생목록', 'playlist', 'pl'])
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """플레이어의 대기열을 표시합니다.
        선택적으로 표시할 페이지를 지정할 수 있습니다. 각 페이지에는 10개의 요소가 있습니다.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty playlist.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle', aliases=['shf', 'sff'])
    async def _shuffle(self, ctx: commands.Context):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove', aliases=['rm'])
    async def _remove(self, ctx: commands.Context, index: int):
        """재생목록에서 노래를 제거합니다."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='loop', aliases=['루프', 'lp'])
    async def _loop(self, ctx: commands.Context):
        """
        현재 재생중인 노래를 반복합니다.
        이 명령을 다시 호출하여 노래의 루프를 해제하십시오.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('현재 재생 중인 음악이 없습니다.')

        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play', aliases=['p', 'm'])
    async def _play(self, ctx: commands.Context, *, search: str):
        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('{} 요청을 처리하는 동안 오류가 발생했습니다'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('음성 채널에 연결되어 있지 않습니다.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('봇은 이미 음성 채널에 있습니다.')

def setup(bot):
    bot.add_cog(Music(bot))