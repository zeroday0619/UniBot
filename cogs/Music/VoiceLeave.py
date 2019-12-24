import discord
from discord.utils import get
from discord.ext import commands


class VoiceLeave(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True, name='leave', aliases=['l', 'lea'])
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"The bot has left {channel}")
            await ctx.send(f"Left {channel}")
        else:
            print("bot was told to leave voice channel, but was not in one")
            await ctx.send(f"제가 음성 채널에 있지 않습니다.")

def setup(bot):
    bot.add_cog(VoiceLeave(bot))