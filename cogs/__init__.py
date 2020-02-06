from discord.ext import commands
from .Manager.ChatDelete import ChatDelete
from .Manager.Mod import Mod
from .Music.music import music
from .Utils.Events import Events
from .Utils.JoinQuit import JoinQuit
from .Utils.UtilCMD import UtilCMD

def setup(bot: commands.Bot):
    bot.add_cog(ChatDelete(bot))
    bot.add_cog(Mod(bot))
    bot.add_cog(music(bot))
    bot.add_cog(Events(bot))
    bot.add_cog(JoinQuit(bot))
    bot.add_cog(UtilCMD(bot))