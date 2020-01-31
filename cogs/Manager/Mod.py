import discord
from discord.ext import commands


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member, *, reason="No reason"):
        embedKick = (
            discord.Embed(
                title="Admin Tools",
                description="Discord 서버 관리 도구",
                color=discord.Color.blurple()
            )
            .add_field(
                name=f"{member.mention} was kicked by {ctx.author.mention}. [{reason}]",
                value="kick"
            )
        )
        await member.kick(reason=reason)
        await ctx.send(
            embed=embedKick
        )
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member, *, reason="No reason"):
        embedBan = (
            discord.Embed(
                title="Admin Tools",
                description="Discord 서버 관리 도구",
                color=discord.Color.blurple()
            )
            .add_field(
                name=f"{member.mention} was banned by {ctx.author.mention}. [{reason}]",
                value="ban"
            )
        )
        await member.ban(reason=reason)
        await ctx.send(
            embed=embedBan
        )

def setup(bot):
    bot.add_cog(Mod(bot))