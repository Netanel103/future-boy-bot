# imports
from asyncio.tasks import sleep, wait, wait_for
from operator import truediv
from typing import Text
import discord
from discord import user
from discord import member
from discord import client
from discord import guild
from discord import activity
from discord import reaction
from discord import channel
from discord import message
from discord.colour import Color
from discord.embeds import Embed
from discord.enums import Status
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands.core import (
    check,
    command,
    has_permissions,
    has_any_role,
    has_role,
)
from discord.ext.commands.errors import (
    ChannelNotReadable,
    CommandNotFound,
    MemberNotFound,
    MissingPermissions,
    MissingRequiredArgument,
)
from discord.flags import Intents
import random
import asyncio
import datetime
import os
import json
import random
from discord.ui import View, button, Button
from discord.ui import Select
from discord.interactions import Interaction
import os
from dotenv import load_dotenv
from discord.ui import InputText, Modal
import colorama
import aiosqlite

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

for folder in os.listdir("./Commands"):
    for file in os.listdir(f"Commands/{folder}"):
        if file.endswith(".py"):
            bot.load_extension(f"Commands.{folder}.{file[:-3]}")
            print(colorama.Fore.GREEN + f"Loaded {file.lower()[:-3]}")

for file in os.listdir(f"./Events"):
    if file.endswith(".py"):
        bot.load_extension(f"Events.{file[:-3]}")
        print(colorama.Fore.GREEN + f"Loaded {file.lower()[:-3]}")

for file in os.listdir(f"./Systems"):
    if file.endswith(".py"):
        bot.load_extension(f"Systems.{file[:-3]}")
        print(colorama.Fore.GREEN + f"Loaded {file.lower()[:-3]}")


@bot.event
async def on_ready():
    print(colorama.Fore.GREEN + f"{bot.user} Is Ready!")

load_dotenv()
bot.run(os.getenv("TOKEN"))
