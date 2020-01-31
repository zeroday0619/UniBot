from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor
import asyncio

import sys
import json
import codecs
import requests
import logging

def color_header(str):
    return '\033[95m' + str + '\033[0m'

prefix = color_header('UniBot || ')

with codecs.open('config.json', 'r', 'utf-8') as json_file:
    data = json.load(json_file)

bot = commands.AutoShardedBot(command_prefix=data["prefix"], case_insensitive=True)

@bot.command()
@commands.is_owner()
async def music_reload(ctx):
    try:
        bot.unload_extension(f"cogs.Music.music")
        bot.load_extension(f"cogs.Music.music")
        await ctx.send("music module got reloaded!")
    except Exception as e:
        print(f"Music module can not be loaded:")
        raise e
@bot.command()
@commands.is_owner()
async def events_reload(ctx):
    try:
        bot.unload_extension(f"cogs.Utils.Events")
        bot.load_extension(f"cogs.Utils.Events")
        await ctx.send("Events module got reloaded!")
    except Exception as e:
        print(f"Events module can not be loaded:")
        raise e

@bot.command()
@commands.is_owner()
async def mod_reload(ctx):
    try:
        bot.unload_extension(f"cogs.Manager.Mod")
        bot.load_extension(f"cogs.Manager.Mod")
        await ctx.send("Mod module got reloaded!")
    except Exception as e:
        print(f"Mod module can not be loaded:")
        raise e


def post_stats():
	payload = {"server_count":int(len(bot.servers))}
	headers = {"Authorization":str(bot.settings.discordbotsorg_token)}
	r = requests.post("https://discordbots.org/api/bots/{}/stats".format(str(bot.user.id)), data=payload, headers=headers)
	if not(r.status_code == 200 or r.status_code == 304):
		bot.logger.error("2/Failed to post server count: " + str(r.status_code))
		bot.logger.error("The following data was returned by the request:\n{}".format(r.text))


def logger_config(bot):
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    log_format = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: ''%(message)s', 
        datefmt='[%I:%M:%S %p]'
    )
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(log_format)
    stdout_handler.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    file_handler = logging.handlers.RotatingFileHandler(
        filename='data/bot/bot.log', 
        encoding='utf-8', 
        mode='a', 
        maxBytes=10 ** 8, 
        backupCount=5
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)
    api_logger = logging.getLogger("discord")
    api_logger.setLevel(logging.WARNING)
    api_handler = logging.FileHandler(
        filename='data/bot/discord.log', 
        encoding='utf-8', 
        mode='a'
    )
    api_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: ''%(message)s', 
            datefmt='[%I:%M:%S %p]'
        )
    )
    api_logger.addHandler(api_handler)

    return logger

running_threads = 0 
max_threads = data['thread']


async def run_in_threadpool(function):
    global running_threads

    while running_threads >= max_threads:
        await asyncio.sleep(1)

    with ThreadPoolExecutor(max_workers=1) as thread_pool:
        running_threads = running_threads + 1

        loop = asyncio.get_event_loop()
        result = loop.run_in_executor(thread_pool, function)
        try:
            result = await result
        except Exception as e:
            raise e
        finally:
            running_threads = running_threads - 1
            thread_pool.shutdown(wait=True)

        return result
