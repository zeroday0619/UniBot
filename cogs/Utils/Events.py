import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        user = message.author
        msg = message.content
        print(f"{user} >> {msg}")

    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            CheckFailure = (
                discord.Embed(
                    title="Permission Error",
                    description="You don't have the permissions to do that!"
                )
            )
            await ctx.send(
                embed=CheckFailure
            )
        if isinstance(error, commands.CommandNotFound):
            CommandNotFound = (
                discord.Embed(
                    title="Command Not Found!",
                    description="This is not a command"
                )
            )
            await ctx.send(
                embed=CommandNotFound
            )

def setup(bot):
    bot.add_cog(Events(bot))