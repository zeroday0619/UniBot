from Util import *
import discord

class UtilCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(title="**UniBot**", description="Team Uni's Discord Bot Project", color=0x00ff00)
        embed.add_field(name="개발자", value="Abel Beak#1955", inline=True)
        embed.add_field(name="사용중 서버 수", value=f"{len(bot.guilds)}", inline=True)
        embed.add_field(name="초대 링크", value="https://discordapp.com/oauth2/authorize?client_id=601614100451295242&permissions=8&scope=bot", inline=True)
        await ctx.send(embed=embed)


    bot.remove_command('help')
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="**UniBot 사용 설명서**", description="", color=0x00ff00)
        embed.add_field(name="$botinfo", value="UniBot에 대한 정보를 확인합니다.")
        embed.add_field(name="$serverinfo", value="{} 채널에 대한 정보를 확인합니다.".format(ctx.guild.name))
        embed.add_field(name="$userinfo [유저]", value="유저에 대한 정보를 확인합니다.")
        # embed.add_field(name="$serverinfo", value="")
        # embed.add_field(name="$add X Y", value="Gives the addition of **X** and **Y**", inline=False)
        # embed.add_field(name="$multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
        # embed.add_field(name="$greet", value="Gives a nice greet message", inline=False)
        # embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
        # embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
        # embed.add_field(name="$help", value="Gives this message", inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed(title="", descriptions="", color=0x00ff00)
        embed.set_author(name="{} 채널 정보".format(ctx.guild.name))
        embed.add_field(name="Name", value=ctx.guild.name, inline=True)
        embed.add_field(name="ID", value=ctx.guild.id, inline=True)
        embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
        embed.add_field(name="Members", value=len(ctx.guild.members))
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        user = ctx.author
        if member is not None:
            user = member
        embed = discord.Embed(title="{}'s Info".format(user.name), description="", color=0x00ff00)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Highest role", value=user.top_role)
        embed.add_field(name="Joined", value=user.joined_at)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
