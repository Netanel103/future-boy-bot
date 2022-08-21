import discord
from discord.ext import commands
import typing


class invite(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="invite")
    @commands.has_permissions(administrator=True)
    async def _invite(
        self,
        ctx: commands.Context,
        member: typing.Union[discord.Member, discord.User] = None,
        uses: int = None,
    ):
        if member is None:
            return await ctx.send("Please mention a member!")
        elif uses is None:
            return await ctx.send("Please enter number of uses for the invite!")
        else:
            invite = await ctx.guild.channels[0].create_invite(max_uses=uses)
            try:
                await member.send(f"{invite}")

                await ctx.send(f"I sent to {member} this invite: {invite}")
            except Exception as e:
                print(e)
                await ctx.send(
                    f"I couldn't send the invite to {member}...\nMaybe DM closed"
                )
                return


def setup(bot: commands.Bot):
    bot.add_cog(invite(bot))