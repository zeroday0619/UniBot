from discord.ext import commands
from DataManager import ConfigManager

def color_header(str):
    return '\033[95m' + str + '\033[0m'

prefix = color_header('UniBot || ')

bot = commands.Bot(command_prefix='$')

cfg = ConfigManager.load_config()