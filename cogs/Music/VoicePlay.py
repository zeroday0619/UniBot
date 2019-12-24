import discord
import youtube_dl

from discord.utils import get
from discord.ext import commands
from youtube_dl import YoutubeDL

class VoicePlay(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True, name='play', aliases=['p', 'm'])
    async def _play(self, ctx, search:str):
        ytdlopts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': False,
            'no_warnings': False,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'no-geo-bypass': True,
        }
        ffmpegopts = {
            'before_options': '-nostdin',
            'options': '-vn'
        }
        ytdl = YoutubeDL(ytdlopts)
        try:
            data = ytdl.extract_info(url=search, download=True)
        except youtube_dl.utils.YoutubeDLError:
            await asyncio.sleep(1)
        
        if 'entries' in data:
            data = data['entries'][0]

        Yt = ytdl.prepare_filename(data)
        await ctx.send("Getting everything ready now")
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        print("Downloading audio now\n")
        voice.play(discord.FFmpegPCMAudio(Yt), after=lambda e: ctx.send(f"{data['title']} has finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        await ctx.send(f"[Playing] : {data['title']}")
        print("Playing")
    


def setup(bot):
    bot.add_cog(VoicePlay(bot))