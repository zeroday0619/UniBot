
import discord
from Music import Music
from Util import *


@bot.command()
async def info(ctx):
    embed = discord.Embed(title="**UniBot**", description="Team Uni's Discord Bot Project", color=0xeee657)
    embed.add_field(name="개발자", value="Abel Beak#1955")
    embed.add_field(name="사용중 서버 수", value=f"{len(bot.guilds)}")
    embed.add_field(name="초대 링크", value="https://discordapp.com/oauth2/authorize?client_id=601614100451295242&permissions=8&scope=bot")
    await ctx.send(embed=embed)



bot.remove_command('help')
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="**UniBot 사용 설명서**", description="", color=0xeee657)
    # embed.add_field(name="$add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    # embed.add_field(name="$multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    # embed.add_field(name="$greet", value="Gives a nice greet message", inline=False)
    # embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    # embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
    # embed.add_field(name="$help", value="Gives this message", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def m(ctx, *, reason: Music):
    await ctx.send(reason)

