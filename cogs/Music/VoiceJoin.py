from discord.utils import get
from discord.ext import commands

import discord

class VoiceJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True, name='join', aliases=['j'])
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        
        if voice and voice.is_connected():
            # Move to voice channel
            await voice.move_to(channel)
        else:
            # Connect to voice channel
            voice = await channel.connect()
        # Disconnect Voice Channel   
        await voice.disconnect()
    
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print("The bot has connected to "+f"{channel}\n")
        
        await ctx.send(f"Joined {channel}")

def setup(bot):
    bot.add_cog(VoiceJoin(bot))