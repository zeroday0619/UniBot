import random
from discord.ext import commands

class Music(commands.Converter):

    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return '{0.author} slapped {1} because *{2}*'.format(ctx, to_slap, argument)

    # async def connect(self):
    #
    # async def playing(self):
    #
    # async def skip(self):
    #
    # async def purge(self):
    #
    # async def stop(self):
    #
    # async def join(self):
    #
    # async def quit(self):
