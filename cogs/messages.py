from discord.ext import commands
from services.get_player_data import *
from services.post_player_data import *
from bot import bot, CHANNEL_ID

class Messages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        get_channelid = int(CHANNEL_ID) #The chnnelid must be an int
        '''If message starts with thumbsup then 
        add the player to the playing list'''
        if message.author == self.bot.user:
            return
        if message.content.startswith('👍') and message.channel.id == get_channelid:
                tally = player_count()
                count = 10 - tally
                if count > 0:
                    try:
                        available_players = []
                        available_players.append(message.author.display_name) #Update tally expects an array
                        update_tally(available_players)
                        print("Player is in:", message.author.display_name)
                        new_tally = player_count()
                        new_count = 10 - new_tally
                        msg = f'You are on the team {message.author.display_name}. There are {new_count} places remaining'
                        await message.channel.send(msg)
                    except:
                        print("Couldn't find player", message.author.display_name)
                        msg = f"Couldn't find player {message.author.display_name}."
                        await message.channel.send(msg)
                else:
                    msg = "Sorry there are no places left this week."
                    await message.channel.send(msg)
        if message.content.startswith('👎') and message.channel.id == get_channelid:
            '''If message starts with thumbsdown then 
            remove the player to the playing list'''
            try:
                available_players = []
                available_players.append(message.author.display_name) #Modify tally expects an array
                modify_tally(available_players)
                print("Player is out:", message.author.display_name)
                tally = player_count()
                count = 10 - tally
                msg = f'Now we have {count} places left. Hopefully see you next week {message.author.display_name}'
                await message.channel.send(msg)
            except:
                print("Couldn't find player", message.author.display_name)
                msg = f"Couldn't find player {message.author.display_name}."
                await message.channel.send(msg)

def setup(bot):
    bot.add_cog(Messages(bot))