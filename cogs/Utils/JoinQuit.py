from Util import *

class JoinQuit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.channel.send('{} 님이 서버에 참가하셨습니다!'.format(member.mention))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await member.channel.send('{} 님이 서버에서 퇴장하셨습니다!'.format(member.mention))

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     # print(message)
    #     # if message == "ㄴㅎ":
    #     await message.channel.send("?")

    # @commands.Cog.listener()
    # async def on_server_join(self, server):
    #     try:
    #         post_stats()
    #         await bot.change_presence(game=discord.Game(name='!!help • {} Guilds'.format(len(bot.servers))),status=discord.Status.online)
    #     except:
    #         self.logger.error(traceback.format_exc())
    #         logging.info("Joined server {0.name} (ID: {0.id})".format(server))
    #     try:
    #         await bot.send_message(server.default_channel, ':wave: Hi, I\'m NanoBot! For help on what I can do, type `!!help`. Join the NanoBot Discord for support and updates: https://discord.io/nano-bot')
    #     except:
    #         pass
    #     await bot.send_message(bot.get_channel(id="334385091482484736"), embed=bot.embeds.server_join(server))
    #
    #
    # @bot.event
    # async def on_server_remove(self, server):
    #     try:
    #         post_stats()
    #         await bot.change_presence(game=discord.Game(name='!!help • {} Guilds'.format(len(bot.servers))), status=discord.Status.online)
    #     except:
    #         self.logger.error(traceback.format_exc())
    #     logging.info("Left server {0.name} (ID: {0.id})".format(server))
    #     await bot.send_message(bot.get_channel(id="334385091482484736"), embed=bot.embeds.server_leave(server))