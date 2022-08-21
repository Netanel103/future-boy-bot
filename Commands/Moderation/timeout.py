import discord
from discord.ext import commands
import humanfriendly
import asyncio
import datetime

class timeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="timeout")
    @commands.has_permissions(administrator=True)
    async def timeout(
        self,
        ctx: commands.Context,
        member: discord.Member = None,
        time=None,
        *,
        reason=None,
    ):
        if member is None:
            em = discord.Embed(
                title="Timeout Error ❌",
                description=f"**Please Tag a member to Timeout!**",
                color=0xFF0000,
            )
            await ctx.send(embed=em)
            return True
        if member == self.bot.user:
            em2 = discord.Embed(
                title="Timeout Error ❌",
                description=f"**I cant Timeout myself!**",
                color=0xFF0000,
            )
            await ctx.send(embed=em2)
            return True
        if member == ctx.author:
            em3 = discord.Embed(
                title="Timeout Error ❌",
                description=f"**You cant Timeout youself!**",
                color=0xFF0000,
            )
            await ctx.send(embed=em3)
            return True
        # if the member has administrator permission
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Timeout Error ❌",
                description=f"I cant Timeout member with administrator permissions",
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
        if time is None:
            em4 = discord.Embed(
                title="Timeout Error ❌",
                description=f"**Please specify a time!**",
                color=0xFF0000,
            )
            await ctx.send(embed=em4)
            return True
        if reason == None:
            reason = "No reason provided"

        time = humanfriendly.parse_timespan(time)
        await member.timeout(
            until=discord.utils.utcnow() + datetime.timedelta(seconds=time),
            reason=reason,
        )
        newtime = humanfriendly.format_timespan(time)
        embed = discord.Embed(
            title="Timeout Success!",
            description=f"**__User:__** \n {member.mention} | **Was Timed Out** \n \n **__Timed Out By:__** \
                \n {ctx.author.mention} \n \n **__Reason:__** \n {reason} \n\n **__Time:__** \n ``{newtime}``",
            color=discord.Color.green(),
            timestamp=ctx.message.created_at,
        )
        embed.set_footer(
            text=f"Timeout By: {ctx.author.name}#{ctx.author.discriminator}",
            icon_url=ctx.author.display_avatar,
        )
        await ctx.send(embed=embed)
        await asyncio.sleep(time)
        print(f"{member.name} Unmuted")
        print(f"Message Created at: {ctx.message.created_at.timestamp()}")

    @timeout.error
    async def timeout_err(self, ctx, err):
        print(err)


def setup(bot: commands.Bot):
    bot.add_cog(timeout(bot))
