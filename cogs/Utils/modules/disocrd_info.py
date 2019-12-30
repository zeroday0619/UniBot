from Util import *

class _disocrd_info(bot):
    def __init__(self, ctx):
        self._bot = bot
        self._guild = bot.guilds
        self._latency = bot.latency # Measures latency between a HEARTBEAT and a HEARTBEAT_ACK in seconds.

    
    def guild_count(self):

        guild_c = str(len(self._bot.guilds))
        print(guild_c)
        return guild_c
    
    def server_user_count(self):
        
disocrd_info = _disocrd_info(bot)