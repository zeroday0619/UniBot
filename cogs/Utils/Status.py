from discord.ext import commands
from discord.ext import tasks
import discord
import asyncio





class StatusView(commands.Cog):
    """ Uni 봇이 디스코드 서버 접속 --> stats 카테고리 생성 --> 접속한 서버의 유저 수 봇 수를 보이스채널 명으로 생성
        채널 명:
            Discord Server 유저 수
            Disocrd Server bot 수
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.category_name = "STATS"
        
    @task.loop(minutes=5.0)
    async def ChangeStatistics(self, guild: discord..Guild):

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        print("Created Category")
        await guild.create_category(name=self.category_name)
        await guild.create_voice_channel(name="TEST", category=self.category_name)
        
