from Util import *
import asyncio

class ChatDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_contxt=True)
    # @commands.has_permissions(administrator=True)
    async def clear(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit+1)
        await ctx.send('{}님이 {}개의 채팅을 청소하셨습니다.'.format(ctx.author.mention, limit))
        # await ctx.message.delete()

    # @clear.error
    # async def clear_error(ctx, error):
    #     if isinstance(error, commands.MissingPermissions):
    #         await ctx.send("You cant do that!")