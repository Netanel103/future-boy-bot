import discord
from discord.ext import commands
from discord.ui import View, button, Button
from discord.ui import Select
from discord.interactions import Interaction


class kickCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            em = discord.Embed(
                title="Kick Error ❌",
                description=f"**Please Tag a member to kick!**",
                color=0xFF0000,
            )
            await ctx.send(embed=em)
            return True
        if member == self.bot.user:
            em2 = discord.Embed(
                title="Kick Error ❌",
                description=f"**I cant kick myself!**",
                color=0xFF0000,
            )
            await ctx.send(embed=em2)
            return True
        if member == ctx.author:
            em3 = discord.Embed(
                title="Kick Error ❌",
                description=f"**You cant kick youself!**",
                color=0xFF0000,
            )
            await ctx.send(embed=em3)
            return True
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Kick Error ❌",
                description=f"I cant kick member with administrator permissions",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return True
        if member.top_role > ctx.author.top_role:
            return await ctx.send(
                embed=discord.Embed(
                    title="Kick Error ❌",
                    description=f"{member.mention} has higher role than you.",
                    color=0xFF0000,
                )
            )
        if reason == None:
            reason = "No reason provided"
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Kick Success!",
            description=f"**__User:__** \n \n {member} | **Was Kicked** \n \n **__Kicked By:__** \n {ctx.author.mention} \n \n **__Reason:__** \n {reason}",
            color=discord.Color.green(),
            timestamp=True,
        )
        embed.set_footer(
            text=f"Kicked By: {ctx.author.name}#{ctx.author.discriminator}",
            icon_url=ctx.author.display_avatar,
        )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(kickCog(bot))
