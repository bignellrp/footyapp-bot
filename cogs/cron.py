from discord.ext import commands
import aiocron
from services.post_player_data import wipe_tally
from bot import bot, CHANNEL_ID

class Cron(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @aiocron.crontab('00 08 * * THU')
    # @commands.Cog.listener()
    # async def cronmsg():
    #     get_channelid = int(CHANNEL_ID) #The chnnelid must be an int
    #     channel = bot.get_channel(get_channelid) #Should not be hardcoded
    #     wipe_tally()
    #     await channel.send('Whos available to play this week?')

def setup(bot):
    bot.add_cog(Cron(bot))