import discord
from discord.ext import commands
import humanfriendly


class errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            return await ctx.send(
                embed=discord.Embed(
                    title="Command Error ❌",
                    description="You don't have the required role to use this command!",
                    color=0xFF0000,
                    timestamp=ctx.message.created_at,
                ).set_footer(
                    text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar
                )
            )
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(
                embed=discord.Embed(
                    title="Command Error ❌",
                    description="You don't have the required permissions to use this command!",
                    color=0xFF0000,
                    timestamp=ctx.message.created_at,
                ).set_footer(
                    text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar
                )
            )
        elif isinstance(error, commands.MissingRole):
            return await ctx.send(
                embed=discord.Embed(
                    title="Command Error ❌",
                    description="You don't have the required role to use this command!",
                    color=0xFF0000,
                    timestamp=ctx.message.created_at,
                ).set_footer(
                    text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar
                )
            )
        elif isinstance(error, commands.CommandOnCooldown):
            time = error.retry_after.__int__()
            format_time = humanfriendly.format_timespan(time)
            await ctx.send(
                embed=discord.Embed(
                    title="Command Cooldown ❌",
                    description=f"Oops, an error ouccured! \n `This Command Is On Cooldown... Please try again in {format_time}`",
                    color=0xFF0000,
                )
            )


def setup(bot: commands.Bot):
    bot.add_cog(errors(bot))
