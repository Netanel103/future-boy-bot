import discord
from discord.ext import commands
import asyncio
from discord.ui import View, Button, button
from discord.interactions import Interaction
from discord.ui import Select, select
from discord.ui import Modal, InputText


# global params
categoryId = 1010860851315613797
logsChannel = 1010860995897462866
membersRole = 1009832326173306940
staffRole = ...
highStaffRole = ...
managersRole = ...
discordManagersRole = ...
ownersRole = 1009831782985773166  # Role Name: Admin



class userModal(Modal):
    def __init__(self):
        super().__init__(title="Add User", custom_id="usermodal")
        self.add_item(
            InputText(
                label="User ID",
                placeholder="ONLY THE USER ID",
                style=discord.InputTextStyle.short,
            )
        )

    async def callback(self, interaction: Interaction):
        channel = interaction.channel
        user = interaction.guild.get_member(int(self.children[0].value))
        overwrites = discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            attach_files=True,
            embed_links=True,
        )
        await channel.set_permissions(user, overwrite=overwrites, reason="Added user")
        await interaction.response.send_message(
            content=f"Successfully Added {user.mention} to The Ticket!", ephemeral=False
        )
        logschannel = interaction.guild.get_channel(logsChannel)
        await logschannel.send(
            embed=discord.Embed(
                title="Ticket Logs - User Added",
                description=f"",
                color=discord.Color.orange(),
                timestamp=interaction.message.created_at,
            )
            .add_field(name="User:", value=user.mention, inline=True)
            .add_field(name="Added By:", value=interaction.user.mention, inline=True)
            .add_field(name="Ticket Channel:", value=interaction.channel.name)
            .set_thumbnail(url=interaction.guild.icon.url)
            .set_footer(text="User Added at", icon_url=interaction.user.display_avatar)
        )


class removeModal(Modal):
    def __init__(self):
        super().__init__(title="Remove User", custom_id="remove")
        self.add_item(
            InputText(
                label="User ID",
                placeholder="ONLY THE USER ID",
                style=discord.InputTextStyle.short,
            )
        )

    async def callback(self, interaction: Interaction):
        channel = interaction.channel
        user = interaction.guild.get_member(int(self.children[0].value))
        overwrites = discord.PermissionOverwrite(
            view_channel=False,
            send_messages=False,
            attach_files=False,
            embed_links=False,
        )
        await channel.set_permissions(user, overwrite=overwrites, reason="Added user")
        await interaction.response.send_message(
            content=f"Successfully Removed {user.mention} From The Ticket!",
            ephemeral=True,
        )
        logschannel = interaction.guild.get_channel(logsChannel)
        await logschannel.send(
            embed=discord.Embed(
                title="Ticket Logs - User Removed",
                description=f"",
                color=discord.Color.dark_red(),
                timestamp=interaction.message.created_at,
            )
            .add_field(name="User:", value=user.mention, inline=True)
            .add_field(name="Removed By:", value=interaction.user.mention, inline=True)
            .add_field(name="Ticket Channel:", value=interaction.channel.name)
            .set_thumbnail(url=interaction.guild.icon.url)
            .set_footer(
                text="User Removed at", icon_url=interaction.user.display_avatar
            )
        )


class renameModal(Modal):
    def __init__(self):
        super().__init__(title="Rename Ticket Channel", custom_id="rename")
        self.add_item(
            InputText(
                label="Channel Name",
                placeholder="Channel Name Here...",
                style=discord.InputTextStyle.short,
            )
        )

    async def callback(self, interaction: Interaction):
        logschannel = interaction.guild.get_channel(logsChannel)
        await logschannel.send(
            embed=discord.Embed(
                title="Ticket Logs - Ticket Renamed",
                description=f"{interaction.user.mention} Renamed a ticket channel",
                color=discord.Color.blurple(),
                timestamp=interaction.message.created_at,
            )
            .add_field(
                name="Channel Name Before:",
                value=f"{interaction.channel.name}",
                inline=True,
            )
            .add_field(
                name="Channel Name After:",
                value=f"{self.children[0].value}",
                inline=True,
            )
            .set_thumbnail(url=interaction.guild.icon.url)
            .set_footer(
                text="Channel Renamed at", icon_url=interaction.user.display_avatar
            )
        )
        await interaction.channel.edit(name=self.children[0].value)
        await interaction.response.send_message(
            content=f"Successfully changed the channel name to {self.children[0].value}!",
            ephemeral=True,
        )


class closeModal(Modal):
    def __init__(self):
        super().__init__(title="Close Ticket Reason", custom_id="close")
        self.add_item(
            InputText(
                label="Reason",
                placeholder="Reason Here...",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: Interaction):
        channel = interaction.guild.get_channel(logsChannel)
        await channel.send(
            embed=discord.Embed(
                title="Ticket Logs - Ticket Closed",
                description="",
                color=discord.Color.red(),
                timestamp=interaction.message.created_at,
            )
            .add_field(
                name="Closed By:", value=f"{interaction.user.mention}", inline=True
            )
            .add_field(name="Ticket Channel", value=f"{interaction.channel.name}")
            .add_field(name="Reason", value=self.children[0].value)
            .set_thumbnail(url=interaction.guild.icon.url)
            .set_footer(text="Ticket Closed at", icon_url=interaction.guild.icon.url)
        )
        await interaction.channel.delete(reason=f"{self.children[0].value}")
        await interaction.response.send_message("Closed The Ticket", ephemeral=True)


class ticketSelects(Select):
    def __init__(self):
        super().__init__()


class ticketMenu(View):
    def __init__(self):
        self.value = None
        super().__init__(timeout=None)

    @button(
        label="Add User", style=discord.ButtonStyle.blurple, emoji="👥", custom_id="user"
    )
    async def addUserCallback(self, button: Button, interaction: Interaction):
        await interaction.response.send_modal(userModal())

    @button(
        label="Remove User",
        style=discord.ButtonStyle.red,
        emoji="❌",
        custom_id="removeuser",
    )
    async def callback(self, button: Button, interaction: Interaction):
        await interaction.response.send_modal(removeModal())

    @button(
        label="Rename Channel",
        style=discord.ButtonStyle.blurple,
        emoji="📝",
        custom_id="rename",
    )
    async def rename_callback(self, button: Button, interaction: Interaction):
        await interaction.response.send_modal(renameModal())

    @button(
        label="Close Ticket",
        style=discord.ButtonStyle.red,
        emoji="🗑",
        custom_id="close",
    )
    async def close_callback(self, button: Button, interaction: Interaction):
        await interaction.response.send_modal(closeModal())


class ticketChannelButtons(View):
    def __init__(self):
        self.value = None
        super().__init__(timeout=None)

    @button(
        label="Claim Ticket",
        style=discord.ButtonStyle.green,
        emoji="🙋‍♂️",
        custom_id="claimbtn",
    )
    async def claim_callback(self, button: Button, interaction: Interaction):
        roles = [
            # interaction.user.get_role(staffRole),  # staff
            # interaction.user.get_role(highStaffRole),  # high staff
            # interaction.user.get_role(managersRole),  # managers
            # interaction.user.get_role(discordManagersRole),  # discord managers
            interaction.user.get_role(ownersRole),  # owners
        ]
        if any(roles):
            button.label = f"Claimed By: {interaction.user}"
            button.disabled = True
            await interaction.channel.edit(
                topic=f"🙋‍♂️ Claimed Ticket | Ticket Claimed By: {interaction.user}"
            )
            await interaction.response.edit_message(view=self)
            logschannel = interaction.guild.get_channel(logsChannel)
            await logschannel.send(
                embed=discord.Embed(
                    title="Ticket Logs - Ticket Claimed",
                    description=f"",
                    color=discord.Color.green(),
                    timestamp=interaction.message.created_at,
                )
                .add_field(name="User:", value=interaction.user.mention, inline=True)
                .add_field(name="Ticket Channel:", value=interaction.channel.name)
                .set_thumbnail(url=interaction.guild.icon.url)
                .set_footer(
                    text="Ticket Claimed at", icon_url=interaction.user.display_avatar
                )
            )
        else:
            await interaction.response.send_message(
                content="You dont have the permissions to do that!", ephemeral=True
            )

    @button(
        label="Ticket options",
        style=discord.ButtonStyle.blurple,
        emoji="💂‍♂️",
        custom_id="staffmenu",
    )
    async def staffmenu(self, button: Button, interaction: Interaction):
        roles = [
            # interaction.user.get_role(staffRole),  # staff
            # interaction.user.get_role(highStaffRole),  # high staff
            # interaction.user.get_role(managersRole),  # managers
            # interaction.user.get_role(discordManagersRole),  # discord managers
            interaction.user.get_role(ownersRole),  # owners
        ]
        if any(roles):
            await interaction.response.send_message(
                embed=discord.Embed(
                    title=f"{interaction.guild.name} - Ticket Staff Menu",
                    description=f"שלום {interaction.user.mention}, ברוך הבא לתפריט הצוות.\n**כאן, תוכל לנהל את הטיקט לפי אופציות.**\n **__אופציות:__**\n> 1. Add User - להוסיף משתמש לפי האיידי של המשתמש\n> 2. Remove User - להוריד משתמש מהטיקט לפי האיידי של המשתמש\n> 3. Rename Ticket - לשנות את השם של הטיקט\n> 4. Close Ticket - לסגור את הטיקט",
                    color=discord.Color.blurple(),
                )
                .set_thumbnail(url=interaction.guild.icon.url)
                .set_footer(
                    text="Requested by: {}".format(interaction.user),
                    icon_url=interaction.user.display_avatar,
                ),
                view=ticketMenu(),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "You dont have the permissions to do this!", ephemeral=True
            )


class staffMenu(View):
    def __init__(self):
        self.value = None
        super().__init__(timeout=None)


class suggestionModal(Modal):
    def __init__(self):
        super().__init__(title="Suggestion", custom_id="sug")
        self.add_item(
            InputText(
                label="Your Suggestion",
                placeholder="כאן אתה יכול לרשום את ההצעה שלך. בבקשה תרשום את ההצעה במפורט",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: Interaction):
        chars = "!@#$%^&*()<>?./"
        name = str(interaction.user.name)
        for char in chars:
            name = name.replace(char, "")
        ticket_channel = discord.utils.find(
            lambda n: n.name == f"suggestion-{name}",
            interaction.guild.text_channels,
        )
        if ticket_channel:
            await interaction.response.send_message(
                content="**אתה לא יכול לפתוח יותר מטיקט אחד.**", ephemeral=True
            )
        else:
            await interaction.response.send_message("יוצר את הטיקט...", ephemeral=True)
            channel = await interaction.guild.create_text_channel(
                name=f"suggestion-{name}",
                category=discord.utils.get(interaction.guild.categories, id=categoryId),
                reason=f"{interaction.user} Opened a ticket!",
                overwrites={
                    interaction.user: discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        attach_files=True,
                        embed_links=True,
                    ),  # the user
                    interaction.guild.get_role(
                        membersRole
                    ): discord.PermissionOverwrite(
                        view_channel=False
                    ),  # members
                    # interaction.guild.get_role(staffRole): discord.PermissionOverwrite(
                    #     view_channel=False,
                    # ),  # staff
                    # interaction.guild.get_role(
                    #     highStaffRole
                    # ): discord.PermissionOverwrite(
                    #     view_channel=True,
                    #     send_messages=True,
                    #     attach_files=True,
                    #     embed_links=True,
                    # ),  # high staff
                    # interaction.guild.get_role(
                    #     managersRole
                    # ): discord.PermissionOverwrite(
                    #     view_channel=True,
                    #     send_messages=True,
                    #     attach_files=True,
                    #     embed_links=True,
                    # ),  # managers
                    interaction.guild.default_role: discord.PermissionOverwrite(
                        view_channel=False
                    ),
                },
            )
            await interaction.edit_original_message(
                content=f"הטיקט שלך נוצר בהצלחה!\nהטיקט: {channel.mention}",
            )
            # staffMention = await channel.send(
            #     content=interaction.guild.get_role(staffRole).mention
            # )
            await asyncio.sleep(1)
            # await staffMention.delete()
            msg = await channel.send(
                content=interaction.user.mention,
                embed=discord.Embed(
                    title=f"{interaction.guild.name} - Ticket Suggestion 💡",
                    description=f"**שלום {interaction.user.mention} וברוך הבא לטיקט ההצעה שלך!**\n**ההצעה:**\n**{self.children[0].value}**",
                    colour=discord.Colour.purple(),
                    timestamp=interaction.message.created_at,
                )
                .set_thumbnail(url=interaction.guild.icon.url)
                .set_footer(
                    text=f"Ticket Created at",
                    icon_url=interaction.user.display_avatar,
                ),
                view=ticketChannelButtons(),
            )
            await msg.pin()
            logschannel = interaction.guild.get_channel(logsChannel)
            await logschannel.send(
                embed=discord.Embed(
                    title=f"Ticket Created",
                    description=f"{interaction.user.mention} Created a ticket channel!",
                    color=discord.Color.green(),
                    timestamp=interaction.message.created_at,
                )
                .add_field(name="User", value=interaction.user.mention)
                .add_field(
                    name="Ticket Channel",
                    value=f"{channel.mention} ({channel.name})",
                )
                .add_field(name="Type", value="Staff Test")
                .set_thumbnail(url=interaction.guild.icon.url)
                .set_footer(
                    text=f"Ticket Created at",
                    icon_url=f"{interaction.user.display_avatar}",
                )
            )


class otherModal(Modal):
    def __init__(self):
        super().__init__(title="Reason For Opening", custom_id="reason")
        self.add_item(
            InputText(
                label="Reason",
                placeholder=f"כאן אתה יכול לרשום  את הסיבה שלך",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: Interaction):
        chars = "!@#$%^&*()<>?./"
        name = str(interaction.user.name)
        for char in chars:
            name = name.replace(char, "")
        ticket_channel = discord.utils.find(
            lambda n: n.name == f"other-{name}",
            interaction.guild.text_channels,
        )
        if ticket_channel:
            await interaction.response.send_message(
                content="**אתה לא יכול לפתוח יותר מטיקט אחד.**", ephemeral=True
            )
        else:
            await interaction.response.send_message("יוצר את הטיקט...", ephemeral=True)
            channel = await interaction.guild.create_text_channel(
                name=f"other-{name}",
                category=discord.utils.get(interaction.guild.categories, id=categoryId),
                reason=f"{interaction.user} Opened a ticket!",
                overwrites={
                    interaction.user: discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        attach_files=True,
                        embed_links=True,
                    ),  # the user
                    interaction.guild.get_role(
                        membersRole
                    ): discord.PermissionOverwrite(
                        view_channel=False
                    ),  # members
                    # interaction.guild.get_role(staffRole): discord.PermissionOverwrite(
                    #     view_channel=False,
                    # ),  # staff
                    # interaction.guild.get_role(
                    #     highStaffRole
                    # ): discord.PermissionOverwrite(
                    #     view_channel=True,
                    #     send_messages=True,
                    #     attach_files=True,
                    #     embed_links=True,
                    # ),  # high staff
                    # interaction.guild.get_role(
                    #     managersRole
                    # ): discord.PermissionOverwrite(
                    #     view_channel=True,
                    #     send_messages=True,
                    #     attach_files=True,
                    #     embed_links=True,
                    # ),  # managers
                    interaction.guild.default_role: discord.PermissionOverwrite(
                        view_channel=False
                    ),
                },
            )
            # staffMention = await channel.send(
            #     content=interaction.guild.get_role(staffRole).mention
            # )
            await asyncio.sleep(1)
            # await staffMention.delete()
            await interaction.edit_original_message(
                content=f"הטיקט שלך נוצר בהצלחה!\nהטיקט: {channel.mention}",
            )
            msg = await channel.send(
                content=interaction.user.mention,
                embed=discord.Embed(
                    title=f"{interaction.guild.name} - Ticket Other",
                    description=f"**שלום {interaction.user.mention} וברוך הבא לטיקט הדיווח שלך!**\n**כאן תוכל לדווח על תקלה בשרת.**\n**סיבת פתיחת הטיקט:**\n**{self.children[0].value}**",
                    colour=discord.Colour.purple(),
                    timestamp=interaction.message.created_at,
                )
                .set_thumbnail(url=interaction.guild.icon.url)
                .set_footer(
                    text=f"Ticket Created at",
                    icon_url=interaction.user.display_avatar,
                ),
                view=ticketChannelButtons(),
            )
            await msg.pin()
            logschannel = interaction.guild.get_channel(logsChannel)
            await logschannel.send(
                embed=discord.Embed(
                    title=f"Ticket Created",
                    description=f"{interaction.user.mention} Created a ticket channel!",
                    color=discord.Color.green(),
                    timestamp=interaction.message.created_at,
                )
                .add_field(name="User", value=interaction.user.mention)
                .add_field(
                    name="Ticket Channel",
                    value=f"{channel.mention} ({channel.name})",
                )
                .add_field(name="Type", value="Other")
                .set_thumbnail(url=interaction.guild.icon.url)
                .set_footer(
                    text=f"Ticket Created at",
                    icon_url=f"{interaction.user.display_avatar}",
                )
            )


class ticketSelectsView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @select(
        placeholder="נא לבחור אופציה",
        custom_id="ticket_options",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="עזרה מהצוות",
                description=f"טיקט לקבלת עזרה מצוות השרת",
                emoji="❓",
                value="help",
            ),
            discord.SelectOption(
                label="הצעה",
                description=f"טיקט להצעה חדשה לשרת",
                emoji="💡",
                value="sug",
            ),
            discord.SelectOption(
                label="אחר",
                description=f"טיקט לכל מה שאתם צריכים. חובה לרשום סיבה לפתיחת הטיקט",
                value="other",
                emoji="⚙",
            ),
        ],
    )
    async def callback(self, select: Select, interaction: Interaction):
        chars = "!@#$%^&*()<>?./"
        name = str(interaction.user.name)
        for char in chars:
            name = name.replace(char, "")
        if select.values[0] == "help":
            ticket_channel = discord.utils.find(
                lambda n: n.name == f"help-{name}",
                interaction.guild.text_channels,
            )
            if ticket_channel:
                await interaction.response.send_message(
                    content="**אתה לא יכול לפתוח יותר מטיקט אחד.**", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "יוצר את הטיקט...", ephemeral=True
                )
                channel = await interaction.guild.create_text_channel(
                    name=f"help-{name}",
                    category=discord.utils.get(
                        interaction.guild.categories, id=categoryId
                    ),
                    reason=f"{interaction.user} Opened a ticket!",
                    overwrites={
                        interaction.user: discord.PermissionOverwrite(
                            view_channel=True,
                            send_messages=True,
                            attach_files=True,
                            embed_links=True,
                        ),  # the user
                        interaction.guild.get_role(
                            membersRole
                        ): discord.PermissionOverwrite(
                            view_channel=False
                        ),  # members
                        # interaction.guild.get_role(
                        #     staffRole
                        # ): discord.PermissionOverwrite(
                        #     view_channel=False,
                        # ),  # staff
                        # interaction.guild.get_role(
                        #     highStaffRole
                        # ): discord.PermissionOverwrite(
                        #     view_channel=True,
                        #     send_messages=True,
                        #     attach_files=True,
                        #     embed_links=True,
                        # ),  # high staff
                        # interaction.guild.get_role(
                        #     managersRole
                        # ): discord.PermissionOverwrite(
                        #     view_channel=True,
                        #     send_messages=True,
                        #     attach_files=True,
                        #     embed_links=True,
                        # ),  # managers
                        interaction.guild.default_role: discord.PermissionOverwrite(
                            view_channel=False
                        ),
                    },
                )
                await interaction.edit_original_message(
                    content=f"הטיקט שלך נוצר בהצלחה!\nהטיקט: {channel.mention}",
                )
                # staffMention = await channel.send(
                #     content=interaction.guild.get_role(staffRole).mention
                # )
                await asyncio.sleep(1)
                # await staffMention.delete()
                msg = await channel.send(
                    content=interaction.user.mention,
                    embed=discord.Embed(
                        title=f"{interaction.guild.name} - Ticket Help",
                        description=f"**שלום {interaction.user.mention} וברוך הבא לטיקט העזרה שלך!**\n***בבקשה תפרט מה אתה צריך ותחכה בסבלנות לצוות.***",
                        colour=discord.Colour.purple(),
                        timestamp=interaction.message.created_at,
                    )
                    .set_thumbnail(url=interaction.guild.icon.url)
                    .set_footer(
                        text=f"Ticket Created at",
                        icon_url=interaction.user.display_avatar,
                    ),
                    view=ticketChannelButtons(),
                )
                await msg.pin()
                logschannel = interaction.guild.get_channel(logsChannel)
                await logschannel.send(
                    embed=discord.Embed(
                        title=f"Ticket Created",
                        description=f"{interaction.user.mention} Created a ticket channel!",
                        color=discord.Color.green(),
                        timestamp=interaction.message.created_at,
                    )
                    .add_field(name="User", value=interaction.user.mention)
                    .add_field(
                        name="Ticket Channel",
                        value=f"{channel.mention} ({channel.name})",
                    )
                    .add_field(name="Type", value="Help")
                    .set_thumbnail(url=interaction.guild.icon.url)
                    .set_footer(
                        text=f"Ticket Created at",
                        icon_url=f"{interaction.user.display_avatar}",
                    )
                )
        elif select.values[0] == "sug":
            await interaction.response.send_modal(suggestionModal())

        elif select.values[0] == "other":
            await interaction.response.send_modal(otherModal())


class ticketButton(View):
    def __init__(self):
        self.value = None
        super().__init__(timeout=None)

    @button(
        style=discord.ButtonStyle.gray,
        custom_id="ticketbtn",
        emoji="📨",
    )
    async def create_callback(self, button: Button, interaction: Interaction):
        await interaction.response.send_message(
            embed=discord.Embed(
                title=f"{interaction.guild.name} - Ticket System Options",
                description=f"שלום {interaction.user.mention} וברוך הבא לאופציות פתיחת הטיקט!\n**כדי לפתוח טיקט בנושא כלשהו, בחר אחד מהנושאים למטה 👇**",
                colour=discord.Colour.purple(),
            )
            .set_thumbnail(url=interaction.guild.icon.url)
            .set_footer(
                text=f"{interaction.guild.name} - Ticket Options",
                icon_url=f"{interaction.guild.icon.url}",
            ),
            view=ticketSelectsView(),
            ephemeral=True,
        )


class tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ticketButton())
        self.bot.add_view(ticketChannelButtons())

    @commands.command(name="ticketmsg", aliases=["ticket"])
    @commands.has_permissions(administrator=True)
    async def _ticket(self, ctx: commands.Context):
        await ctx.message.delete()
        await ctx.send(
            embed=discord.Embed(
                title=f"{ctx.guild.name} - Ticket System",
                description=f"**בכדי לפתוח טיקט אנא לחצו על הכפתור למטה 📨**",
                colour=discord.Colour.blue(),
            )
            .set_footer(
                text=f"{ctx.guild.name} - Ticket System",
                icon_url=ctx.guild.icon.url,
            )
            .set_thumbnail(url=ctx.guild.icon.url),
            view=ticketButton(),
        )

    @_ticket.error
    async def ticket_error(self, ctx, err):
        print(err)


def setup(bot: commands.Bot):
    bot.add_cog(tickets(bot))
