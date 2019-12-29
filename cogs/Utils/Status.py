from discord.ext import commands
import discord
from Util import *


class StatusView(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild_count = str(len(self.bot.guilds))
        status_view = "Server: "+guild_count
        await guild.create_voice_channel(name=status_view)
def setup(bot):
    bot.add_cog(StatusView(bot))


        

    