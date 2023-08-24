import os
import discord
import discord.ext.commands as commands
from dotenv import load_dotenv

##Load our environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN_DEV")

##Initialise our client
client = discord.Client()

##Initialise our app and the bot itself
##https://discordpy.readthedocs.io/en/latest/intents.html
intents = discord.Intents.default()
intents.members = True

## Set up the bot
bot = commands.Bot(command_prefix='$', intents=intents)

##Register Cogs with Discord
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

##Register Cogs with Discord
client.run(TOKEN)