import discord
from discord.ext import commands


class unTimeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="remtimeout", aliases=["removetimeout", "untimeout"])
    @commands.has_permissions(administrator=True)
    async def removetimeout(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            em = discord.Embed(
                title="Timeout Error ❌",
                description=f"**Please Tag a member to Timeout!**",
                color=0xFF0000,
            )
            await ctx.send(embed=em)
            return True
        if not member.timed_out:
            await ctx.send(
                embed=discord.Embed(
                    title="Error ❌",
                    description="{} is not On Timeout".format(member.mention),
                    color=ctx.author.color,
                    timestamp=ctx.message.created_at,
                ).set_footer(text=f"Error ❌", icon_url=ctx.author.display_avatar)
            )
            return True
        await member.remove_timeout(
            reason=f"{ctx.author.name}#{ctx.author.discriminator} Removed the timeout for {member}"
        )
        embed = discord.Embed(
            title="Successfully Removed Timeout!",
            description=f"**Successfully Removed The Timeout for:** {member.mention}",
            color=member.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_footer(
            text=f"Removed The Timeout By: {ctx.author.name}#{ctx.author.discriminator}",
            icon_url=ctx.author.display_avatar,
        )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(unTimeout(bot))
