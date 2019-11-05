from discord.ext import commands
import json
import codecs

def color_header(str):
    return '\033[95m' + str + '\033[0m'

prefix = color_header('UniBot || ')

with codecs.open('config.json', 'r', 'utf-8') as json_file:
    data = json.load(json_file)

bot = commands.Bot(command_prefix=data["prefix"])
