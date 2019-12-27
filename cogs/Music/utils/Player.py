import asyncio
import itertools
import sys
import traceback
import discord
from discord.ext import commands
from async_timeout import timeout
from functools import partial

from .YTDLSource import YTDLSource

class Player:
	"""
	Base class for Music Player
	"""
	__slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

	def __init__(self, ctx):
		self.bot = ctx.bot
		self._guild = ctx.guild
		self._channel = ctx.channel
		self._cog = ctx.cog

		self.queue = asyncio.Queue()
		self.next = asyncio.Event()

		self.np = None
		self.volume = .5
		self.current = None

		ctx.bot.loop.create_task(self.player_loop())

	async def player_loop(self):
		await self.bot.wait_until_ready()

		while not self.bot.is_closed():
			self.next.clear()

			try:
				async with timeout(300):
					source = await self.queue.get()
			except asyncio.TimeoutError as TimeoutError:
				print(str(TimeoutError))
				return self.destroy(self._guild)

			if not isinstance(source, YTDLSource):
				try:
					source = await YTDLSource.reqather_stream(source, loop=self.bot.loop)
				except Exception as e:
					await self._channel.send("Error: {}".format(e))
					continue

			source.volume = self.volume
			self.current = source
			embed = (
				discord.Embed(
					title='Now playing', description='```css\n{0.title}\n```'.format(source),
					color=discord.Color.blurple()
				)
					.add_field(name='Duration', value=self.current.duration)
					.add_field(name='Requested by', value=self.current.requester)
					.add_field(name='Uploader', value='[{0.uploader}]({0.uploader_url})'.format(self.current))
					.add_field(name='URL', value='[Click]({0.web_url})'.format(self.current))
					.set_thumbnail(url=self.current.thumbnail)
			)
			self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
			self.np = await self._channel.send(embed=embed)
			await self.next.wait()

			source.cleanup()
			self.current = None


			try:
				await self.np.delete()
			except discord.HTTPException as HTTPException:
				await self._channel.send("Error: {}".format(HTTPException))

	def destroy(self, guild):
		# Disconnect and Cleanup
		return self.bot.loop.create_task(self._cog.cleanup(guild))