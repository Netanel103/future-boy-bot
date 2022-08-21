import discord
from discord.ext import commands
import datetime


class welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(1009888813151166624)

        await channel.send(
            content=member.mention,
            embed=discord.Embed(
                title=f"Welcome To {member.guild.name}!",
                description=f"""
                **ברוך הבא ל {member.guild.name}!**
                בבקשה תקרא את {member.guild.get_channel(963357841782104114).mention} לפני שאתה מתחיל לדבר בשרת!
                חוויה נעימה!
                """,
                color=discord.Color.purple(),
                timestamp=datetime.datetime.utcnow(),
            )
            .set_thumbnail(url=member.display_avatar)
            .set_image(url="https://images-ext-1.discordapp.net/external/CW9_z9ll_PRxdgn2o9xjC6Vx-ocNLI8vju8tm1leGbQ/%3Fsize%3D1024/https/cdn.discordapp.com/icons/959835109052280902/920412d3533b8a93a4007c19a2a5da45.png")
            .set_footer(icon_url=member.display_avatar),
        )


def setup(bot: commands.Bot):
    bot.add_cog(welcome(bot))
