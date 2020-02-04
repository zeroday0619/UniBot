import discord
import asyncio
from discord.ext import commands
from discord.ext import tasks
from app import alert

twitch = alert()
app = twitch.polling(
    client_id="", 
    client_secret="", 
    name=""
)
print(app)