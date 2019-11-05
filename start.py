from Util import *
from Cogs import JoinQuit
from Cogs import Command
import discord

@bot.event
async def on_ready():
    """
    봇이 실행되었을때 발생하는 이벤트, 봇이 켜졌다는 신호의 이벤트임.
    :return:
    """
    print(prefix + "Uni Bot이 실행되고 있습니다!")
    print(prefix + "Bot Name: {}".format(bot.user.name))
    print(prefix + "Join Server(Guild) List:")
    for g in bot.guilds:
        print(prefix + "\t- " + g.name)


if __name__ == '__main__':
    activity = discord.Activity(name='my activity', type=discord.ActivityType.watching)
    # bot.change_presence(activity=activity)

    bot.remove_command('help')
    bot.add_cog(JoinQuit.JoinQuit(bot))
    bot.add_cog(Command.Command(bot))

    bot.run(data["token"])
