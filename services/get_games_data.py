import requests

games_api_url = "http://localhost:8080/games"
response = requests.get(games_api_url)

def game_stats():

    if response.status_code == 200:
        games = response.json()

        # Sort players by name in alphabetical order
        # This might not work until date is converted in the api
        sorted_games = sorted(games, key=lambda game: game["date"])

        # Create the player_totals list with name and total
        game_stats = [
            {
                "date" : game["date"],
                "scoreTeamA" : game["scoreTeamA"],
                "scoreTeamB" : game["scoreTeamB"]
            } 
            for game in sorted_games
        ]
        return game_stats
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []
    
def most_recent_game():
    if response.status_code == 200:
        games = response.json()

        # Sort games by date in descending order
        # This might not work until date is converted in the api
        sorted_games = sorted(games, key=lambda game: game["date"], reverse=True)

        if sorted_games:
            most_recent_game = sorted_games[0]
            game_data = {
                "date": most_recent_game["date"],
                "teamA": most_recent_game["teamA"],
                "teamB": most_recent_game["teamB"],
                "scoreTeamA": most_recent_game["scoreTeamA"],
                "scoreTeamB": most_recent_game["scoreTeamB"],
                "totalTeamA": most_recent_game["totalTeamA"],
                "totalTeamB": most_recent_game["totalTeamB"],
                "colourTeamA": most_recent_game["colourTeamA"],
                "colourTeamB": most_recent_game["colourTeamB"]
            }
            return [game_data]
        else:
            print("No games found.")
            return []
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def teama():

    if response.status_code == 200:
        games = response.json()
        date = "2023-08-15"
        list = [game["teamA"] for game in games if game.get("date") == date]
        return list
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def teamb():

    if response.status_code == 200:
        games = response.json()
        date = "2023-08-15"
        list = [game["teamB"] for game in games if game.get("date") == date]
        return list
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def scorea():

    if response.status_code == 200:
        games = response.json()
        date = "2023-08-15"
        value = [game["scoreTeamA"] for game in games if game.get("date") == date]
        value = ', '.join(map(str, value))
        return value
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def scoreb():

    if response.status_code == 200:
        games = response.json()
        date = "2023-08-15"
        value = [game["scoreTeamB"] for game in games if game.get("date") == date]
        value = ', '.join(map(str, value))
        return value
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def totala():

    if response.status_code == 200:
        games = response.json()
        date = "2023-08-15"
        value = [game["totalTeamA"] for game in games if game.get("date") == date]
        value = ', '.join(map(str, value))
        return value
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def totalb():

    if response.status_code == 200:
        games = response.json()
        date = "2023-08-15"
        value = [game["totalTeamB"] for game in games if game.get("date") == date]
        value = ', '.join(map(str, value))
        return value
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def coloura():

    if response.status_code == 200:
        games = response.json()
        date = "2023-08-15"
        value = [game["colourTeamA"] for game in games if game.get("date") == date]
        value = ', '.join(map(str, value))
        return value
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def colourb():

    if response.status_code == 200:
        games = response.json()
        date = "2023-08-15"
        value = [game["colourTeamB"] for game in games if game.get("date") == date]
        value = ', '.join(map(str, value))
        return value
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

game_stats = game_stats()
print("Game Stats:", game_stats)

teama = teama()
print("TeamA:", teama)

teamb = teamb()
print("TeamB:", teamb)

scorea = scorea()
print("Score Team A:", int(scorea))

scoreb = scoreb()
print("Score Team B:", int(scoreb))

totala = totala()
print("Total Team A:", int(totala))

totalb = totalb()
print("Total Team B:", int(totalb))

coloura = coloura()
print("Colour Team A:", coloura)

colourb = colourb()
print("Colour Team B:", colourb)

most_recent_game = most_recent_game()
print("Most Recent Game:", most_recent_game)