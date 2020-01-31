import discord
import asyncio
import youtube_dl
import functools
import itertools
from discord import FFmpegPCMAudio
from discord import PCMVolumeTransformer
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Cog
from discord.ext.commands import Context
from discord.ext.commands import CommandError
from asyncio import BaseEventLoop
from youtube_dl import YoutubeDL
from cogs.Music.utils.option import ffmpeg_options
from cogs.Music.utils.option import ytdl_format_options
from Util import run_in_threadpool

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl = YoutubeDL(ytdl_format_options)

class YTDLDownloadOnly(CommandError):
    """Only download"""

class YTDLSource(PCMVolumeTransformer):
    def __init__(self, source, *, data, requester):
        super().__init__(source)
        date = data.get('upload_date')
        self.url = data.get('url')  # Youtube Addresses
        self.web_url = data.get('webpage_url')
        self.data = data # Youtube Content Data
        self.title = data.get('title') # Youtube Title
        self.thumbnail = data.get('thumbnail') # Youtube Thumbnail
        self.requester = requester
        self.uploader = data.get('uploader') # Youtube Uploader
        self.uploader_url = data.get('uploader_url')
        self.description = data.get('description')

        self.duration = self.parse_duration(int(data.get('duration')))
    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)
    @classmethod
    async def Search(cls, ctx: Context, search: str, *, loop: BaseEventLoop = None, download=True):
        loop = loop or asyncio.get_event_loop()
        try:
            data = await run_in_threadpool(lambda: ytdl.extract_info(url=search, download=download))
        except youtube_dl.utils.YoutubeDLError as ytdl_error:
            await ctx.send("Error: {}".format(str(ytdl_error)))

        if 'entries' in data:
            data = data['entries'][0]

        await ctx.send("**{}**가 재생목록에 추가되었습니다.".format(str(data['title'])))

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}
        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)


    @classmethod
    async def reqather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']
        source = await run_in_threadpool(lambda: ytdl.extract_info(url=data['webpage_url'], download=False))
        return cls(discord.FFmpegPCMAudio(source['url']), data=source, requester=requester)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))
        return ', '.join(duration)
