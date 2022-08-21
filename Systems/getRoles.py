import discord
from discord.ext import commands
from discord.ui import View, Select, select
from discord.interactions import Interaction


class rolesMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @select(
        placeholder="לחצו בשביל לבחור רול!",
        custom_id="roles",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="High Level",
                emoji="<a:8LevelUp:530430817395015691>",
                value="high_level",
                description="בחרו את האופציה כדי לקחת את הרול",
            ),
            discord.SelectOption(
                label="Low Level",
                emoji="<:down:853449660567650334>",
                value="low_level",
                description="בחרו את האופציה כדי לקחת את הרול",
            ),
            discord.SelectOption(
                label="Operating Systems",
                emoji="<:pc:829731463804485653>",
                description="בחרו את האופציה כדי לקבל את הרול",
                value="operating_systems",
            ),
        ],
    )
    async def callback(self, select: Select, interaction: Interaction):
        if select.values[0] == "high_level":
            role = interaction.guild.get_role(1009886647975944263)
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(
                    content=f"הורדתי לך את הרול {role.mention}", ephemeral=True
                )
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    f"קיבלת את הרול {role.mention}", ephemeral=True
                )
        elif select.values[0] == "low_level":
            role = interaction.guild.get_role(1009886779026968676)
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(
                    content=f"הורדתי לך את הרול {role.mention}", ephemeral=True
                )
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    f"קיבלת את הרול {role.mention}", ephemeral=True
                )
        elif select.values[0] == "operating_systems":
            role = interaction.guild.get_role(1009886515368824882)
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(
                    content=f"הורדתי לך את הרול {role.mention}", ephemeral=True
                )
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    f"קיבלת את הרול {role.mention}", ephemeral=True
                )


class getRoles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(rolesMenu())
        print("Loaded roles Menu")

    @commands.command(name="getroles")
    @commands.has_permissions(administrator=True)
    async def _getroles(self, ctx: commands.Context):
        await ctx.message.delete()
        await ctx.send(
            embed=discord.Embed(
                title=f"{ctx.guild.name} - Get Roles",
                description=f""" 
                שימו לב, במידה ותלחצו על האופציות כל פעם שבן אדם יבקש עזרה בנושא מסויים תקבלו התראה

**לחצו על האופציה - High level \nכדי לקבל את הרול {ctx.guild.get_role(1009886647975944263).mention}**

**לחצו על האופציה - Low level \nכדי לקבל את הרול {ctx.guild.get_role(1009886779026968676).mention}**

**לחצו על האופציה - Operating systems \nכדי לקבל את הרול {ctx.guild.get_role(1009886515368824882).mention}**
                """,
                color=discord.Color.blurple(),
            ).set_image(
                url="https://images-ext-2.discordapp.net/external/06ClgM7q8HkKcXPVF1W1HDA06NYeLrWHzBZVXwJn83I/https/images-ext-1.discordapp.net/external/CW9_z9ll_PRxdgn2o9xjC6Vx-ocNLI8vju8tm1leGbQ/%253Fsize%253D1024/https/cdn.discordapp.com/icons/959835109052280902/920412d3533b8a93a4007c19a2a5da45.png"
            ),
            view=rolesMenu(),
        )

    @_getroles.error
    async def get_roles_err(self, ctx, err):
        print(err)


def setup(bot: commands.Bot):
    bot.add_cog(getRoles(bot))
