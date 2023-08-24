import requests

player_api_url = "http://localhost:8080/players"
response = requests.get(player_api_url)

def player_names():

    if response.status_code == 200:
        players = response.json()

        # Sort players by name in alphabetical order
        sorted_players = sorted(players, key=lambda player: player["name"])

        # Create the player_totals list with name and total
        player_names = [
            {"name" : player["name"],"playing" : player["playing"]} for player in sorted_players
        ]
        return player_names
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def all_players():

    if response.status_code == 200:
        players = response.json()

        # Sort players by name in alphabetical order
        sorted_players = sorted(players, key=lambda player: player["name"])

        # Create the player_totals list with name and total
        player_totals = [
            {"name" : player["name"], "total" : player["total"]} for player in sorted_players
        ]
        return player_totals
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def player_stats():

    if response.status_code == 200:
        players = response.json()

        # Sort players by name in alphabetical order
        sorted_players = sorted(players, key=lambda player: player["name"])

        # Create the player_stats list with name, wins, draws, losses, score and winpercent
        player_stats = [{
            "name" : player["name"], 
            "wins" : player["wins"],
            "draws" : player["draws"],
            "losses" : player["losses"],
            "score" : player["score"],
            "winpercent" : player["winpercent"]
            } for player in sorted_players
        ]
        return player_stats
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def leaderboard():

    if response.status_code == 200:
        players = response.json()

        # Sort players by score in descending order
        sorted_players = sorted(players, key=lambda player: player["score"], reverse=True)
        
        # Select the top 10 players
        top_players = sorted_players[:10]

        # Create the leaderboard list with name and score
        leaderboard = [
            {"name" : player["name"],"score" : player["score"]} for player in top_players
        ]
        return leaderboard
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []
    
def winpercentage():

    if response.status_code == 200:
        players = response.json()

        # Sort players by name in alphabetical order
        sorted_players = sorted(players, key=lambda player: player["winpercent"])

        # Create the player_totals list with name and total
        player_winpercentages = [
            {"name" : player["name"], "winpercent" : player["winpercent"]} for player in sorted_players
        ]
        return player_winpercentages
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []
    
def player_count():

    if response.status_code == 200:
        players = response.json()
        # Create the playing_players list with name
        playing_players = [
            {player["name"]} for player in players if player.get("playing")
        ]
        return len(playing_players)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def game_player_tally():

    if response.status_code == 200:
        players = response.json()
        # Create the playing_players list with name
        playing_players = [
            {player["name"]} for player in players if player.get("playing")
        ]
        return playing_players
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

player_names = player_names()
player_names = [(player["name"]) for player in player_names]
print("Player Names:", player_names)

totals = all_players()
print("Totals:", totals)

stats = player_stats()
print("Stats:", stats)

leaderboard = leaderboard()
print("Leaderboard:", leaderboard)

winpercentages = winpercentage()
print("Winpercentages:", winpercentages)

player_count = player_count()
print("Player Count:", player_count)

game_player_tally = game_player_tally()
print("Game Player Tally:", game_player_tally)