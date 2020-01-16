import asyncio
import discord
import traceback
import itertools
import sys

from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Cog
from discord.ext.commands import NoPrivateMessage
from cogs.Music.Utils.YTDLSource import YTDLSource
from cogs.Music.Utils.Player import Player
from cogs.Music.Utils.option import embed_ERROR, embed_queued, embed_value


class Music(Cog):
	__slots__ = ('bot', 'players')

	def __init__(self, bot: Bot):
		self.bot = bot
		self.players = {}

	async def cleanup(self, guild):
		try:
			await guild.voice_client.disconnect()
		except AttributeError as AError:
			print("Error: {}".format(str(AError)))
			pass

		try:
			del self.players[guild.id]
		except KeyError as KError:
			print("Error: {}".format(str(KError)))
			pass

	async def __local_check(self, ctx):
		if not ctx.guild:
			raise NoPrivateMessage
		return True

	async def __error(self, ctx, error):
		if isinstance(error, NoPrivateMessage):
			try:
				return await ctx.send("이 Command 는 DM 에서 사용할 수 없습니다")
			except discord.HTTPException as HTTPException:
				try:
					await ctx.send("Error: {}".format(str(HTTPException)))
					pass
				except Exception as Ex:
					print("Error: {}".format(str(Ex)))
					pass
		elif isinstance(error, InvalidVoiceChannel):
			try:
				await ctx.send("Voice Channel 연결중 Error 가 발생하였습니다\n 자신이 Voice Channel에 접속되어 있는 지 확인 바랍니다.")
			except Exception as Ex2:
				print("Error: {}".format(str(Ex2)))
		print('Ignoring exception in command {}'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

	def get_player(self, ctx):
		try:
			player = self.players[ctx.guild.id]
		except KeyError as KError2:
			player = Player(ctx)
			self.players[ctx.guild.id] = player
		return player

	@commands.command(name='connect', aliases=['join', 'j'])
	async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
		if not channel:
			try:
				channel = ctx.author.voice.channel
			except AttributeError as AError2:
				try:
					await ctx.send("Error: {}".format(str(AError2)))
				except discord.HTTPException as He:
					print("Error: {}".format(str(He)))
					pass
				raise InvalidVoiceChannel("Voice channel에 연결하지 못하였습니다.\n 유효한 Voice Channel과 자신이 Voice Channel에 들어와 있는지 확인바랍니다.")
		vc = ctx.voice_client
		if vc:
			if vc.channel.id == channel.id:
				return
			try:
				await vc.move_to(channel)
			except asyncio.TimeoutError as TimeoutError:
				try:
					await ctx.send("Error: {}".format(str(TimeoutError)))
				except discord.HTTPException as He2:
					print("Error: {}".format(str(He2)))
					pass
				raise VoiceConnectionError("Moving to channel: <{}> timed out".format(str(channel)))
		else:
			try:
				await channel.connect()
			except asyncio.TimeoutError as TimeoutError2:
				try:
					await ctx.send("Error: {}".format(str(TimeoutError2)))
				except discord.HTTPException as He3:
					print("Error: {}".format(str(He3)))
					pass
				raise VoiceConnectionError("Connecting to channel: <{}> timed out".format(str(channel)))

		embed_join = (
			(
				discord.Embed(
					title="Music", description='```css\nConnected to **{}**\n```'.format(str(channel)),
					color=discord.Color.blurple()
				)
			)
				.add_field(name="INFO", value="stable")
			)
		await ctx.send(embed=embed_join, delete_after=10)

	@commands.command(name='play', aliases=['music', 'm'])
	async def play_(self, ctx, *, search: str):
		await ctx.trigger_typing()
		vc = ctx.voice_client
		if not vc:
			await ctx.invoke(self.connect_)

		player = self.get_player(ctx)

		source = await YTDLSource.Search(ctx, search, loop=self.bot.loop, download=True)

		await player.queue.put(source)


	@commands.command(name='pause')
	async def pause_(self, ctx):
		vc = ctx.voice_client

		if not vc or not vc.is_playing():
			return await ctx.send(embed=embed_ERROR, delete_after=20)
		elif vc.is_paused():
			return
		embed_pause = ((discord.Embed(title="Music", description=f'```css\n**{ctx.author}** : 일시중지.\n```',
		                              color=discord.Color.blurple())).add_field(name="INFO", value="stable"))

		vc.pause()
		await ctx.send(embed=embed_pause)


	@commands.command(name='resume')
	async def resume_(self, ctx):
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send(embed=embed_ERROR, delete_after=20)
		elif not vc.is_paused():
			return

		vc.resume()
		embed_resume = ((discord.Embed(title="Music", description=f'```css\n**{ctx.author}** : 다시재생.\n```',
		                              color=discord.Color.blurple())).add_field(name="INFO", value="stable"))

		await ctx.send(embed_resume)


	@commands.command(name='skip')
	async def skip_(self, ctx):
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send(embed=embed_ERROR, delete_after=20)

		if vc.is_paused():
			pass
		elif not vc.is_playing():
			return

		vc.stop()
		embed_skip = ((discord.Embed(title="Music", description=f'```css\n**{ctx.author}** : 스킵!.\n```',
		                              color=discord.Color.blurple())).add_field(name="INFO", value="stable"))

		await ctx.send(embed=embed_skip)


	@commands.command(name='queue', aliases=['q', 'playlist'])
	async def queue_info(self, ctx):
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send(embed=embed_ERROR, delete_after=20)

		player = self.get_player(ctx)
		if player.queue.empty():
			return await ctx.send(embed=embed_queued)

		upcoming = list(itertools.islice(player.queue._queue, 0, 5))

		fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
		embed_queue=((discord.Embed(title=f'```css\nUpcoming - Next *{len(upcoming)}*\n```', description=fmt,
		                              color=discord.Color.blurple())))


		await ctx.send(embed=embed_queue)


	@commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing'])
	async def now_playing_(self, ctx):
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send(embed=embed_ERROR, delete_after=20)

		player = self.get_player(ctx)
		if not player.current:
			return await ctx.send(embed=embed_ERROR)

		try:
			await player.np.delete()
		except discord.HTTPException:
			pass
		embed_now_playing = ((discord.Embed(title=f'```css\n**Now Playing:** `{vc.source.title}````', description=f'requested by `{vc.source.requester}`',
		                              color=discord.Color.blurple())))

		player.np = await ctx.send(embed=embed_now_playing)


	@commands.command(name='volume', aliases=['vol'])
	async def change_volume(self, ctx, *, vol: float):
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send(embed=embed_ERROR, delete_after=20)

		if not 0 < vol < 101:
			return await ctx.send(embed_value)

		player = self.get_player(ctx)

		if vc.source:
			vc.source.volume = vol / 100

		player.volume = vol / 100
		embed_now_playing = ((discord.Embed(title="Music", description=f'```**`{ctx.author}`**: Set the volume to **{vol}%**````',
		                              color=discord.Color.blurple())))

		await ctx.send(embed=embed_now_playing)


	@commands.command(name='stop')
	async def stop_(self, ctx):
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send(embed=embed_ERROR, delete_after=20)

		await self.cleanup(ctx.guild)

def setup(bot):
	bot.add_cog(Music(bot))
