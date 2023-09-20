import discord
import discord.ext.commands as commands
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('discord').setLevel(logging.ERROR)
logging.getLogger('discord.http').setLevel(logging.WARNING)

load_dotenv()  # Load environment variables from .env

intents = discord.Intents.default()
intents.members = True
command_prefix = os.getenv("COMMAND_PREFIX")
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
TOKEN = os.getenv("DISCORD_TOKEN")

# for file in os.listdir("cogs"):
#     if file.endswith(".py"):
#         name = file[:-3]
#         bot.load_extension(f"cogs.{name}")

CHANNEL_ID = os.getenv("CHANNEL_ID")

bot.load_extension("cogs.login")
bot.load_extension("cogs.welcome")
bot.load_extension("cogs.messages")
bot.load_extension("cogs.admincommands")
bot.load_extension("cogs.commands")
bot.load_extension("cogs.cron")

# Run the bot
bot.run(TOKEN)