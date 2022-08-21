import discord
from discord.ext import commands
import humanfriendly
import asyncio


class mute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="mute")
    @commands.has_permissions(administrator=True)
    async def mute(
        self, ctx, member: discord.Member = None, time: str = None, *, reason=None
    ):
        if member == None:
            embed = discord.Embed(
                title="Mute Error ❌",
                description="**Oops, an error was Occourred! \n You didnt mention a member..** \n `Please tag a member to mute and try again.`",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(text=f"Error ❌", icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return True
        if member == self.bot.user:
            em = discord.Embed(
                title="Mute Error ❌",
                description="**Oops, an error was Occourred! \n I can't mute myself 🙃**",
                timestamp=ctx.message.created_at,
                color=discord.Color.red(),
            )
            embed.set_footer(text=f"Error ❌", icon_url=ctx.author.avatar)
            await ctx.send(embed=em)
            return True
        if member == ctx.author:
            em2 = discord.Embed(
                title="Mute Error ❌",
                description="**Oops, an error was Oocourred! \n You can't mute yourself!**",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at,
            )
            em2.set_footer(text=f"Error ❌", icon_url=ctx.author.avatar)
            return True
        if member.top_role > ctx.author.top_role:
            return await ctx.send(
                embed=discord.Embed(
                    title="Kick Error ❌",
                    description=f"{member.mention} has higher role than you. you cannot mute him...",
                    color=0xFF0000,
                )
            )
        if time is None:
            await ctx.send(
                embed=discord.Embed(
                    title="Mute Error ❌",
                    description=f"Please enter time to mute!",
                    color=discord.Color.red(),
                )
            )
            return
        if reason == None:
            reason = "No reason provided."

        time = humanfriendly.parse_timespan(time)
        newtime = humanfriendly.format_timespan(time)
        MuteRole = discord.utils.get(ctx.guild.roles, name="Muted")
        if not MuteRole:
            await ctx.send("No mutrole found.. creating one")
            MuteRole = await ctx.guild.create_role(name="Muted")
            await member.add_roles(MuteRole)
            emb = discord.Embed(
                title="Mute Success ✔",
                description=f"**__User:__**\n {member} | Was Muted! \n \n **__Muted By:__** \n {ctx.author.mention} \n \n**__Time:__**\n{newtime} \n\n**__Reason:__** \n {reason}",
                color=discord.Color.green(),
            )
            await ctx.send(embed=emb)
            await member.add_roles(MuteRole)
        await member.add_roles(MuteRole)
        embb = discord.Embed(
            title="Mute Success ✔",
            description=f"**__User:__**\n {member} | Was Muted! \n \n **__Muted By:__** \n {ctx.author.mention} \n\n**__Time:__**\n{newtime} \n \n **__Reason:__** \n {reason}",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embb)
        print(f"{ctx.author} muted {member} for {newtime}")
        await asyncio.sleep(time)
        await member.remove_roles(MuteRole)
        print(f"{member} unmuted || mute time: {newtime}")

    @commands.command(name="unmute")
    @commands.has_any_role(
        875170833612554270,
        914241707401424896,
        980433097994666014,
        379972989267214348,
        330070810784169987,
    )
    async def unmute(self, ctx, member: discord.Member = None):
        muteRole = discord.utils.get(ctx.guild.roles, name="Muted")
        if muteRole in member.roles:
            await member.remove_roles(muteRole)
            await ctx.send(f"Successfully unmuted {member.mention}")
            print(f"{ctx.author} unmuted {member}")
        else:
            await ctx.send(f"{member} is not muted!")
            print(f"{ctx.author} tried to unmute {member} but they werent muted")


def setup(bot: commands.Bot):
    bot.add_cog(mute(bot))
