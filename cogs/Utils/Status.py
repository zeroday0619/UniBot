from discord.ext import commands
from discord.ext import tasks
from .modules.disocrd_info import disocrd_info
import discord
import asyncio
from Util import *




class StatusView(commands.Cog):
    """ Uni 봇이 디스코드 서버 접속 --> stats 카테고리 생성 --> 접속한 서버의 유저 수 봇 수를 보이스채널 명으로 생성
        채널 명:
            Discord Server 유저 수
            Disocrd Server bot 수

    
    """
    def __init__(self, ctx, bot: commands.Bot):
        self.bot = bot
        


    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        
        # TODO: 함수로 만들어서 코드 반복 사용을 줄여야 됨
        """
        Example:
            
            async def create_category_stats(self, guild: discord.Guild):
                await guild.create_category(name="stats")

            async def on_guild_join(self, ctx: commands.Context, guild: discord.Guild):
                await create_category()
        """
        await guild.create_category(name="stats")

        
        # stats 카타고리가 생성 여부 확인 후 보이스 채널 생성 and 예외 처리
        if guild.categories['stats']:
            await guild.create_voice_channel(name="")
        else
            await guild.create_category(name="stats")



def setup(bot):
    bot.add_cog(StatusView(bot))

    