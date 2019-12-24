from Util import *
import discord
from cogs.Utils.JoinQuit import JoinQuit
from cogs.Utils.UtilCMD import UtilCMD
from cogs.Manager.ChatDelete import ChatDelete

@bot.event
async def on_ready():
    """
    봇이 실행되었을때 발생하는 이벤트, 봇이 켜졌다는 신호의 이벤트임.
    :return:
    """
    print(prefix + "Uni Bot이 실행되고 있습니다!")
    print(prefix + "Bot Name: {}".format(bot.user.name))
    print(prefix + "Join Server(Guild) List:")
    bot.load_extension("cogs.Music.VoiceJoin")
    bot.load_extension("cogs.Music.VoicePlay")
    bot.load_extension("cogs.Music.VoiceLeave")
    for g in bot.guilds:
        print(prefix + "\t- " + g.name)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Command | $help"))

if __name__ == '__main__':
    # 616161
    bot.remove_command('help')
    bot.add_cog(JoinQuit(bot))
    bot.add_cog(UtilCMD(bot))
    bot.add_cog(ChatDelete(bot))

    bot.run(data["token"])