import discord
from discord.ext import commands
from services.post_player_data import *
from services.post_games_data import *
from services.get_player_data import *
from services.get_games_data import *
from services.get_even_teams import get_even_teams
from services.get_date import gameday
import re
import asyncio

class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, number):
        """Clear messages"""
        number = int(number)
        try:
            await ctx.channel.purge(limit=number)
        except:
            await ctx.send('Couldnt delete these messages!')
    
    @commands.command(pass_context = True)
    @commands.has_permissions(administrator=True)
    async def wipe(self, ctx):
        """Wipe Tally"""
        try:
            wipe_tally()
            await ctx.send('Tally wiped!')
        except:
            await ctx.send('Error: Couldnt wipe tally!')

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def nick(self, ctx, member: discord.Member, nick):
        """Change nickname"""
        player_names = player_names()
        player_names = [pname["name"] for pname in player_names]
        try:
            await member.edit(nick=nick)
            await ctx.send(f'Nickname was changed for {member.mention} ')
        except:
            await ctx.send(f'Error: Theres an issue with that nickname!')
        if nick in player_names:
            await ctx.send(f'{member.mention} is in the player list.')
        else:
            await ctx.send(f'*Note* {member.mention} is not in the player list. Use the *new* command to add them.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def new(self, ctx, *args):
        """Adds player to db"""
        player_names = player_names()
        player_names = [pname["name"] for pname in player_names]
        for new_player in args:
            if not validate_name(new_player):
                print(f'Invalid name: {new_player}. The name must be one word, no spaces, no special characters, and max 15 chars.')
                await ctx.send(f'Invalid name: {new_player}. The name must be one word, no spaces, no special characters, and max 15 chars.')
                continue

            if new_player in player_names:
                print(f'{new_player} already exists!')
                await ctx.send(f'{new_player} already exists!')
            else:
                add_player(new_player)
                await ctx.send(f'Added new player with a generic score of 77: {new_player}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def score(self, ctx, *args):
        """Update score (no args for lineup)"""
        get_teama = teama()
        get_teamb = teamb()
        get_date = date()
        get_scorea = scorea()
        get_scoreb = scoreb()
        get_teama_colour = coloura()
        get_teamb_colour = colourb()
        fileA = discord.File("static/"+get_teama_colour+".png")
        fileB = discord.File("static/"+get_teamb_colour+".png")
        teama = "\n".join(item for item in get_teama)
        teamb = "\n".join(item for item in get_teamb)
        if get_scorea != "-":
            print('Score already entered for this week')
            await ctx.send('Score already entered for this week')
        elif not args:
            print('Display this weeks teams')
            # Embed Message A
            embeda=discord.Embed(
                title="Here were the teams for:"+str(get_date),
                url="http://football.richardbignell.co.uk/score",
                color=discord.Color.dark_green()
            )
            embeda.add_field(name="TeamA (" 
                            + str(get_scorea) 
                            + "):", value=get_teama, 
                            inline=True)
            embeda.set_thumbnail(url="attachment://"+get_teama_colour+".png")
            embeda.set_footer(text="Use the website above to rerun the saved lineup")
            # Embed Message B
            embedb=discord.Embed(
                title="Here were the teams for:"+str(get_date),
                url="http://football.richardbignell.co.uk/score",
                color=discord.Color.dark_green()
            )
            embedb.add_field(name="TeamB (" 
                            + str(get_scoreb) 
                            + "):", value=get_teamb, 
                            inline=True)
            embedb.set_thumbnail(url="attachment://"+get_teamb_colour+".png")
            embedb.set_footer(text="Use the website above to rerun the saved lineup")
            await ctx.send(file=fileA, embed=embeda)
            await ctx.send(file=fileB, embed=embedb)
            await ctx.send("Please enter the score for TeamA: (1 or 2 digits)")
            def check(m):
                match = re.match("(^[0-9]{1,2}$)",m.content)
                return m.channel == ctx.channel and match
            try:
                msg = await self.bot.wait_for("message", 
                                              timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("You didnt enter a 1 or 2 digit number in 60 seconds.")
                return
            else:
                update_scorea = msg.content
                print("Team A Score stored!")
                await ctx.send("Score saved! Please enter the score for TeamB: (1 or 2 digits)")
                def check(m):
                    match = re.match("(^[0-9]{1,2}$)",m.content)
                    return m.channel == ctx.channel and match
                try:
                    msg = await self.bot.wait_for("message", 
                                                  timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("You didnt enter a 1 or 2 digit number in 60 seconds.")
                    return
                else:
                    update_scoreb = msg.content
                    print("Team B Score saved!")
                    score = {
                      "scoreTeamA": update_scorea,
                      "scoreTeamB": update_scoreb
                    }
                    update_result(score)
                    await ctx.send("Scores saved!")
                    return
        else:
            args_count = len(args) #Count the args to use in validation
            #args = list(map(int, args)) #Convert all args in list to ints
            print(args[0])
            print(args[1])
            match_a = re.match("(^[0-9]{1,2}$)",args[0])
            match_b = re.match("(^[0-9]{1,2}$)",args[1])
            if args_count != 2:
                await ctx.send('You must enter 2 scores')
            elif match_a == None or match_b == None:
                await ctx.send('One or more of your scores is not a valid number')
            else:
                update_scorea = args[0]
                update_scoreb = args[1]
                score = {
                    "scoreTeamA": update_scorea,
                    "scoreTeamB": update_scoreb
                }
                update_result(score)
                print("Scores saved!")
                await ctx.send("Scores saved!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def teams(self, ctx):
        """Generate teams"""
        file = discord.File("static/football.png")
        game_player_tally_with_score = game_player_tally_with_score()
        get_scorea = scorea()
        get_date = date()
        count = player_count()
        if count > 0:
            print(f'Not enough players!')
            await ctx.send(f'We still need {count} more players!')
        elif count < 0:
            print('Too many players!')
            await ctx.send("Too many players!")
        else:
            print('Running even teams function!')
            team_a,team_b,team_a_total,team_b_total = get_even_teams(
                game_player_tally_with_score)
            game_json = {
                "date": gameday,
                "teamA": team_a,
                "teamB": team_b,
                "scoreTeamA": None,
                "scoreTeamB": None,
                "totalTeamA": team_a_total,
                "totalTeamB": team_b_total,
                "colourTeamA": "black",
                "colourTeamB": "white"
                }
            team_a = "\n".join(item for item in team_a)
            team_b = "\n".join(item for item in team_b)
            # Embed Message
            embed=discord.Embed(
                title="Here are the teams:",
                url="http://football.richardbignell.co.uk",
                color=discord.Color.dark_green()
            )
            embed.add_field(name="TeamA (" 
                            + str(team_a_total) 
                            + "):", value=team_a, 
                            inline=True)
            embed.add_field(name="TeamB (" 
                            + str(team_b_total) 
                            + "):", value=team_b, 
                            inline=True)
            embed.set_thumbnail(url="attachment://football.png")
            embed.set_footer(text="Enter on the website if you prefer using the link above")
            await ctx.send(file=file, embed=embed)
            await ctx.send("Type *SAVE* to store the results.")
            await ctx.send("*You need to save in 10 seconds or this team will be lost*")
            def check(m):
                return m.content == "SAVE" and m.channel == ctx.channel
            try:
                msg = await self.bot.wait_for("message", 
                                              timeout=10.0, check=check)
            except asyncio.TimeoutError: 
                print("Teams command timeout!")
                await ctx.send("You didnt type SAVE in 10 seconds. Run !teams again")
                return
            else:
                if get_date == gameday and get_scorea == None:
                    update_result(game_json)
                    print("Running update function")
                    await ctx.send(f"Teams Saved!")
                else:
                    append_result(game_json)
                    print("Running append function")
                    await ctx.send(f"Teams Saved!")
                return
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def swap(self, ctx, *args):
        """Swap player"""
        get_player_names = player_names()
        player_names = [pname["name"] for pname in get_player_names]
        get_teama = teama()
        get_teamb = teamb()
        get_scorea = scorea()
        teams = get_teama + get_teamb
        current_player = args[0]
        new_player = args[1]
        if len(args) != 2:
            print('You must have 2 players!')
            await ctx.send('You must have 2 players!')
        elif get_scorea != None:
            print('Game has already been played this week!')
            await ctx.send('Game has already been played this week!')
        elif current_player not in teams:
            print(f'{current_player} is not in the teams list!')
            await ctx.send(f'{current_player} is not in the team list!')
        elif new_player not in player_names:
            print(f'{new_player} is not in the player list!')
            await ctx.send(f'{args[1]} is not in the player list!')
        elif all([current_player in get_teama, new_player in get_teama]):
            print(f'{current_player} and {new_player} are in Team A: {teama}')
            await ctx.send(f'{current_player} and {new_player} are on the same team!')
        elif all([current_player in get_teamb, new_player in get_teamb]):
            print(f'{current_player} and {new_player} are in Team B: {teamb}')
            await ctx.send(f'{current_player} and {new_player} are on the same team!')
        else:
            swap_players(current_player, new_player)
            await ctx.send(f'{current_player} swapped with {new_player}')
            await ctx.send(f'Run command !lineup for updated teams/scores')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lineup(self, ctx):
        """Lineup"""
        get_teama = teama()
        get_teamb = teamb()
        get_totala = totala()
        get_totalb = totalb()
        get_date = date()
        get_teama_colour = coloura()
        get_teamb_colour = colourb()
        fileA = discord.File("static/"+get_teama_colour+".png")
        fileB = discord.File("static/"+get_teamb_colour+".png")
        get_team_a = "\n".join(item for item in get_teama)
        get_team_b = "\n".join(item for item in get_teamb)
        # Embed Message A
        embeda=discord.Embed(
            title="Here were the teams for:"+str(get_date),
            url="http://football.richardbignell.co.uk/score",
            color=discord.Color.dark_green()
        )
        embeda.add_field(name="TeamA (" 
                        + str(get_totala) 
                        + "):", value=get_team_a, 
                        inline=True)
        embeda.set_thumbnail(url="attachment://"+get_teama_colour+".png")
        embeda.set_footer(text="Use the website above to rerun the saved lineup")
        # Embed Message B
        embedb=discord.Embed(
            title="Here were the teams for:"+str(get_date),
            url="http://football.richardbignell.co.uk/score",
            color=discord.Color.dark_green()
        )
        embedb.add_field(name="TeamB (" 
                        + str(get_totalb) 
                        + "):", value=get_team_b, 
                        inline=True)
        embedb.set_thumbnail(url="attachment://"+get_teamb_colour+".png")
        embedb.set_footer(text="Use the website above to rerun the saved lineup")
        await ctx.send(file=fileA, embed=embeda)
        await ctx.send(file=fileB, embed=embedb)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, *args):
        """Add player(Play)"""
        get_player_names = player_names()
        player_names = [pname["name"] for pname in get_player_names]
        for name in args:
            if name in player_names:
                count = player_count()
                if count > 0:
                    ##Should this allow lower case?
                    update_tally(name)
                    print("Player is in:", name)
                    count = player_count()
                    msg = f'{name} is on the team! There are {count} places remaining'
                    await ctx.send(msg)
                else:
                    msg = "Sorry there are no places left this week."
                    await ctx.send(msg)
            else:
                print(f'{name} doesnt exist!')
                await ctx.send(f'{name} is not in the db. Add him using command !new {name}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rem(self, ctx, *args):
        """Remove player(Play)"""
        get_player_names = player_names()
        player_names = [pname["name"] for pname in get_player_names]
        for name in args:
            if name in player_names:
                modify_tally(name)
                print("Player is out:", name)
                count = player_count()
                await ctx.send(f'We now have {count} places. Hopefully see you next week {name}')
            else:
                print(f'{name} doesnt exist!')
                await ctx.send(f'{name} is not in the db. Add him using command !new {name}')

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def manplay(self, ctx, *args):
        """Manual(All list)"""
        # Needs converting to a slash command as too complicate to use
        file = discord.File("static/football.png")
        game_player_tally = game_player_tally_with_score_and_index()
        args_count = len(args) #Count the args to use in validation
        args = list(map(int, args)) #Convert all args in list to ints
        arg_match = all(i <= 10 for i in args) #True if all args are <= 10

        ##If no args added then send playing list so user can choose from list
        if not args:
            await ctx.invoke(self.bot.get_command('play'))
        if args_count != 5:
            await ctx.send('You must enter 5 numbers')
        elif arg_match == False:
            await ctx.send('Number must be 1 - 10')
        else:
            #Get current result data ready to update results
            get_scorea = scorea()
            get_date = date()
            team_a, team_b, team_a_score, team_b_score = [], [], [], []
            for i, p, s in game_player_tally:
                if i in args:
                    team_a.append(p)
                    team_a_score.append(s)
                else:
                    team_b.append(p)
                    team_b_score.append(s)
            team_a_total = sum(team_a_score)
            team_b_total = sum(team_b_score)

            game_json = {
                "date": gameday,
                "teamA": team_a,
                "teamB": team_b,
                "scoreTeamA": None,
                "scoreTeamB": None,
                "totalTeamA": team_a_total,
                "totalTeamB": team_b_total,
                "colourTeamA": "black",
                "colourTeamB": "white"
                }
            team_a = "\n".join(item for item in team_a)
            team_b = "\n".join(item for item in team_b)
            # Embed Message
            embed=discord.Embed(
                title="Here are the teams:",
                url="http://football.richardbignell.co.uk",
                color=discord.Color.dark_green()
            )
            embed.add_field(name="TeamA (" 
                            + str(team_a_total) 
                            + "):", value=team_a, 
                            inline=True)
            embed.add_field(name="TeamB (" 
                            + str(team_b_total) 
                            + "):", value=team_b, 
                            inline=True)
            embed.set_thumbnail(url="attachment://football.png")
            embed.set_footer(text="Enter on the website if you prefer using the link above")
            await ctx.send(file = file, embed=embed)
            # Wait for user to enter SAVE
            await ctx.send("Type *SAVE* to store the results.")
            await ctx.send("*You need to save in 10 seconds or this team will be lost*")
            def check(m):
                return m.content == "SAVE" and m.channel == ctx.channel
            try:
                await self.bot.wait_for("message", 
                                            timeout=10.0, check=check)
            except asyncio.TimeoutError: 
                print("Teams command timeout!")
                await ctx.send("You didnt type SAVE in 10 seconds. Run !man again")
                return
            else:
                if get_date == gameday and get_scorea == None:
                    update_result(game_json)
                    print("Running update function")
                    await ctx.send(f"Teams Saved!")
                else:
                    append_result(game_json)
                    print("Running append function")
                    await ctx.send(f"Teams Saved!")
                return

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def manall(self, ctx, *args):
        """Manual(Play List)"""
        file = discord.File("static/football.png")
        get_all_players = all_players()
        game_player_tally = []
        num = 1
        for player in get_all_players:
            '''Takes in row of all_players 
            and returns list of game_players with index and score'''
            game_player_tally.append((num,player["name"],player["total"]))
            num = num+1
        args_count = len(args) #Count the args to use in validation
        args = list(map(int, args)) #Convert all args in list to ints
        # def match(args):
        #     for i in args:
        #         if re.match("(^[0-9]{1,2}$)", i):
        #             return False #I think this needs to be True
        #     return True

        #If no args added then send all players so user can choose from list
        if not args: 
            await ctx.invoke(self.bot.get_command('allplayers'))
        elif args_count != 10:
            await ctx.send('You must enter 10 numbers')
        else:
            #Get current result data ready to update results
            get_scorea = scorea()
            get_date = date()
            team_a, team_b, team_a_score, team_b_score = [], [], [], []
            for i, p, s in game_player_tally:
                if i in args[:5]:
                    team_a.append(p)
                    team_a_score.append(s)
                elif i in args[5:]:
                    team_b.append(p)
                    team_b_score.append(s)
            team_a_total = sum(team_a_score)
            team_b_total = sum(team_b_score)

            game_json = {
                "date": gameday,
                "teamA": team_a,
                "teamB": team_b,
                "scoreTeamA": None,
                "scoreTeamB": None,
                "totalTeamA": team_a_total,
                "totalTeamB": team_b_total,
                "colourTeamA": "black",
                "colourTeamB": "white"
                }
            team_a = "\n".join(item for item in team_a)
            team_b = "\n".join(item for item in team_b)
            # Embed Message
            embed=discord.Embed(
                title="Here are the teams:",
                url="http://football.richardbignell.co.uk",
                color=discord.Color.dark_green()
            )
            embed.add_field(name="TeamA (" 
                            + str(team_a_total) 
                            + "):", value=team_a, 
                            inline=True)
            embed.add_field(name="TeamB (" 
                            + str(team_b_total) 
                            + "):", value=team_b, 
                            inline=True)
            embed.set_thumbnail(url="attachment://football.png")
            embed.set_footer(text="Enter on the website if you prefer using the link above")
            await ctx.send(file = file, embed=embed)
            # Wait for user to enter SAVE
            await ctx.send("Type *SAVE* to store the results.")
            await ctx.send("*You need to save in 10 seconds or this team will be lost*")
            def check(m):
                return m.content == "SAVE" and m.channel == ctx.channel
            try:
                msg = await self.bot.wait_for("message", 
                                              timeout=10.0, check=check)
            except asyncio.TimeoutError: 
                print("Teams command timeout!")
                await ctx.send("You didnt type SAVE in 10 seconds. Run !man again")
                return
            else:
                if get_date == gameday and get_scorea == None:
                    update_result(game_json)
                    print("Running update function")
                    await ctx.send(f"Teams Saved!")
                else:
                    append_result(game_json)
                    print("Running append function")
                    await ctx.send(f"Teams Saved!")
                return

def setup(bot):
    bot.add_cog(AdminCommands(bot))