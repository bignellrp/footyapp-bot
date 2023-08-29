from discord.ext import commands
from services.get_player_data import *
from services.post_player_data import *
from services.get_oscommand import GITBRANCH, IFBRANCH
from dotenv import load_dotenv
import os

##Load our environment variables
load_dotenv()

class Messages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        '''If branch is dev then use the dev channel id
        This prevents the two bots conflicting with each other'''
        if  IFBRANCH in GITBRANCH:
            CHANNEL_ID = os.getenv("CHANNEL_ID")
        else:
            CHANNEL_ID = os.getenv("CHANNEL_ID_DEV")
        CHANNEL_ID = int(CHANNEL_ID) #Wasnt matching channel.id as a string
        '''If message starts with thumbsup then 
        add the player to the playing list'''
        if message.author == self.bot.user:
            return
        if message.content.startswith('👍') and message.channel.id == CHANNEL_ID:
            try:
                count = player_count()
                if count > 0:
                    update_tally(message.author.display_name)
                    print("Player is in:", message.author.display_name)
                    count = player_count()
                    msg = f'You are on the team {message.author.display_name}. There are {count} places remaining'
                    await message.channel.send(msg)
                else:
                    msg = "Sorry there are no places left this week."
                    await message.channel.send(msg)
            except:
                print("Couldn't find player", message.author.display_name)
                msg = f"Couldn't find player {message.author.display_name}."
                await message.channel.send(msg)
        if message.content.startswith('👎') and message.channel.id == CHANNEL_ID:
            '''If message starts with thumbsdown then 
            remove the player to the playing list'''
            try:
                modify_tally(message.author.display_name)
                print("Player is out:", message.author.display_name)
                players = player_count()
                msg = f'Now we have {players} places left. Hopefully see you next week {message.author.display_name}'
                await message.channel.send(msg)
            except:
                print("Couldn't find player", message.author.display_name)
                msg = f"Couldn't find player {message.author.display_name}."
                await message.channel.send(msg)

def setup(bot):
    bot.add_cog(Messages(bot))