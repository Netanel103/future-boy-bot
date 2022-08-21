import discord
from discord.ext import commands
from discord.ui import View, button, Button
from discord.ui import Select
from discord.interactions import Interaction
import asyncio


class clearCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="clear")
    @commands.has_permissions(administrator=True)
    async def clear(
        self, ctx: commands.Context, limit: int = None, member: discord.Member = None
    ):
        def member_delete(m):
            return m.author == member

        if limit is None:
            embed = discord.Embed(
                title="Clear Error ❌",
                description="**Please enter an amount to the messages you want to clear!**",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                text=f"{self.bot.user.name}", icon_url=ctx.author.display_avatar
            )
            await ctx.send(embed=embed, delete_after=7)
        if 0 < limit < 100:
            await ctx.message.delete()
            if member is None:
                deleted = await ctx.channel.purge(limit=limit)
                await ctx.send(
                    f"Successfuly deleted {len(deleted):,} Messages!", delete_after=5
                )
            else:
                deleted = await ctx.channel.purge(limit=limit, check=member_delete)
                await ctx.send(f"Successfuly deleted {len(deleted):,} Messages From {member}")
        else:
            em = discord.Embed(
                title="Clear Error ❌",
                description="**Oops, i can't clear above 100 messages in a row.**",
                color=discord.Color.random(),
            )
            await ctx.send(embed=em, delete_after=10)

    @clear.error
    async def err(self, ctx, err):
        print(err)


def setup(bot: commands.Bot):
    bot.add_cog(clearCog(bot))
