import discord
from discord.ext import commands
import os
from discord.ui import View, button, Button
from discord.interactions import Interaction


class verifyButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @button(
        label="Verify",
        style=discord.ButtonStyle.green,
        emoji="<a:v_:988352060875489310>",
        custom_id="verifybtn",
    )
    async def callback(self, button, interaction: Interaction):
        role = interaction.guild.get_role(1009832326173306940)
        await interaction.user.add_roles(role)
        if role in interaction.user.roles:
            await interaction.response.send_message(
                "You are already verified!", ephemeral=True
            )
            return
        await interaction.response.send_message(
            "You have been verified!", delete_after=7, ephemeral=True
        )


class verify(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def verify(self, ctx: commands.Context):
        if ctx.author.id != 880003677019062272:
            return await ctx.send("Only The Bot Developer can run this command!")
        else:
            await ctx.message.delete()
            view = verifyButtons()
            await ctx.send(
                embed=discord.Embed(
                    title=f"{ctx.guild.name} | Verification System",
                    description=f"""
ברוכים הבאים לשרת של - **נוער העתיד** 💭 

על מנת לאמת את עצמכם כ {ctx.guild.get_role(1009832326173306940).mention}  בשרת יש ללחוץ על הריאקשן למטה
במידה ונתקלתם בבעיה יש לפנות להנהלת השרת.
👇

                    """,
                    colour=discord.Colour.blurple(),
                )
                .set_footer(text=f"{ctx.guild.name} - Verify System", icon_url=ctx.guild.icon.url)
                .set_image(url="https://images-ext-2.discordapp.net/external/06ClgM7q8HkKcXPVF1W1HDA06NYeLrWHzBZVXwJn83I/https/images-ext-1.discordapp.net/external/CW9_z9ll_PRxdgn2o9xjC6Vx-ocNLI8vju8tm1leGbQ/%253Fsize%253D1024/https/cdn.discordapp.com/icons/959835109052280902/920412d3533b8a93a4007c19a2a5da45.png"),
                view=view,
            )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(verifyButtons())


def setup(bot: commands.Bot):
    bot.add_cog(verify(bot))
