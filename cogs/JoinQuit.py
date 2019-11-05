from Util import *

class JoinQuit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        guild 에 member 가 접속했을때 발생하는 이벤트
        :param member:
        :return:
        """
        await member.channel.send('{} 님이 서버에 참가하셨습니다!'.format(member))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        guild에서 member가 퇴장, 강퇴, 밴이 되었을대 발생하는 이벤트
        :param member:
        :return:
        """
        await member.channel.send('{} 님이 서버에서 퇴장하셨습니다!'.format(member))
