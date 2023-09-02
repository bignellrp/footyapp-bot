import discord
import discord.ext.commands as commands
from dotenv import load_dotenv
from services.get_oscommand import IFBRANCH, GITBRANCH
import os
# import logging

# logging.basicConfig(level=logging.DEBUG)

load_dotenv()  # Load environment variables from .env

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)
TOKEN = os.getenv("DISCORD_TOKEN_DEV")

# for file in os.listdir("cogs"):
#     if file.endswith(".py"):
#         name = file[:-3]
#         bot.load_extension(f"cogs.{name}")

# @bot.event
# async def on_ready():
#     """Adds a message to the log when the bot logs in."""
#     print(f"{bot.user.name} logged in successfully")

if IFBRANCH in GITBRANCH:
    CHANNEL_ID = os.getenv("CHANNEL_ID")
else:
    CHANNEL_ID = os.getenv("CHANNEL_ID_DEV")

bot.load_extension("cogs.login")
bot.load_extension("cogs.welcome")
bot.load_extension("cogs.messages")
bot.load_extension("cogs.admincommands")
bot.load_extension("cogs.commands")
bot.load_extension("cogs.cron")

# Run the bot
bot.run(TOKEN)