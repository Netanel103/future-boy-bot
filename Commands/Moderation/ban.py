import discord
from discord.ext import commands
from discord.ui import View, button, Button
from discord.ui import Select
from discord.interactions import Interaction
import requests
import typing


class banCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ban", case_sensitive=True)
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        member: typing.Union[discord.Member, discord.User] = None,
        *,
        reason=None,
    ):
        if member is None:
            em = discord.Embed(
                title="Ban Error ❌",
                description=f"**Please Tag a member to Ban!**",
                color=0xFF0000,
            )
            await ctx.send(embed=em)
            return True
        if member == self.bot.user:
            em2 = discord.Embed(
                title="Ban Error ❌",
                description=f"**I cant kick myself!**",
                color=0xFF0000,
            )
            await ctx.send(embed=em2)
            return True
        if member == ctx.author:
            em3 = discord.Embed(
                title="Ban Error ❌",
                description=f"**You cant Ban youself!**",
                color=0xFF0000,
            )
            await ctx.send(embed=em3)
            return True

            embed = discord.Embed(
                title="Ban Error ❌",
                description=f"I cant Ban member with administrator permissions",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return True
        if not ctx.author.guild_permissions.ban_members:
            embed = discord.Embed(
                title="Ban Error ❌",
                description=f"I cant Ban member with administrator permissions",
                color=0x303236,
            )
            await ctx.send(embed=embed)
            return True
        if member in ctx.guild.members:
            if member.top_role > ctx.author.top_role:
                return await ctx.send(
                    embed=discord.Embed(
                        title="Ban Error ❌",
                        description=f"{member.mention} has higher role than you.",
                        color=0xFF0000,
                    )
                )
            if reason == None:
                reason = "No reason provided"
            try:
                await ctx.guild.ban(member, reason=reason)
                embed = discord.Embed(
                    title="Ban Success!",
                    description=f"**__User:__**\n {member} **Was Banned** \n \n **__Banned By:__** \n {ctx.author.mention} \n \n **__Reason:__** \n {reason}",
                    color=discord.Color.green(),
                )
                embed.set_footer(
                    text=f"Banned By: {ctx.author.name}#{ctx.author.discriminator}",
                    icon_url=ctx.author.display_avatar,
                )
                await ctx.send(embed=embed)
            except discord.HTTPException as e:
                embed = discord.Embed(
                    title="An Error occurred!",
                    description=e,
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
        else:
            if reason == None:
                reason = "No reason provided"
            try:
                await ctx.guild.ban(member, reason=reason)
                embed = discord.Embed(
                    title="Ban Success!",
                    description=f"**__User:__**\n {member} **Was Banned** \n \n **__Banned By:__** \n {ctx.author.mention} \n \n **__Reason:__** \n {reason}",
                    color=discord.Color.green(),
                )
                embed.set_footer(
                    text=f"Banned By: {ctx.author.name}#{ctx.author.discriminator}",
                    icon_url=ctx.author.display_avatar,
                )
                await ctx.send(embed=embed)
            except discord.HTTPException as e:
                embed = discord.Embed(
                    title="An Error occurred!",
                    description=e,
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, exc):
        if isinstance(exc, commands.BadUnionArgument):
            print(f"Ban Error:\n{exc}")
            await ctx.send("I couldn't find this user id in discord. Sorry.")
            return


def setup(bot: commands.Bot):
    bot.add_cog(banCog(bot))
