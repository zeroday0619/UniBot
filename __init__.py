from Util import *
from DataManager import ConfigManager
import sys
from Event import JoinQuit
from Event import Ready
from Music import Music
import Command

if __name__ == '__main__':
    # bot.remove_command('help')
    # bot.add_cog(Event.JoinQuit)
    # bot.add_cog(Event.Ready)
    bot.add_cog(Command)
    # bot.add_cog(Music.Music)
    bot.run(cfg["token"])

