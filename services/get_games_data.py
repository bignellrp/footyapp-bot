import requests
from dotenv import load_dotenv
import os

##Load the .env file
load_dotenv()

####### JWT AUTH #######
# # Login to the API to get JWT token
# API_USERNAME = os.getenv("API_USERNAME")
# API_PASSWORD = os.getenv("API_PASSWORD")

# # Url used for login
# login_api_url = "http://localhost:8080/login"

# response = requests.post(login_api_url, json={"username": API_USERNAME, "password": API_PASSWORD})
# access_token = response.json()["access_token"]
# access_headers = {
#     "Authorization": f"Bearer {access_token}"
# }
#########################
#########################


# Create auth header
access_token = os.getenv("API_TOKEN")
access_headers = {
             "Authorization": f"Bearer {access_token}"
         }
api_url = os.getenv("API_URL")
# Url used for games data
games_api_url = f"{api_url}/games"

def game_stats():
    response = requests.get(games_api_url + "/" + "game_stats", headers=access_headers)
    if response.status_code == 200:
        #Example output:
        #[('2023-08-30', 30, 20), ('2023-08-16', 3, 2), ('2023-08-15', 3, 2)]
        data = response.json()
        data = [(game["date"], game["scoreTeamA"], game["scoreTeamB"]) for game in data]
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def game_wins(player):
    response = requests.get(games_api_url + "/wins/" + player, headers=access_headers)
    if response.status_code == 200:
        #Count games where the player is in teamA and scoreTeamA is greater than scoreTeamB
        data = response.json()
        data = data["wins"]
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def game_stats_with_context():
    response = requests.get(games_api_url, headers=access_headers)
    if response.status_code == 200:
        # Example output:
        # [
        #     {
        #         "date": "2023-08-30",
        #         "teamA": ["Player 1", "Player 2", "Player 3"],
        #         "teamB": ["Player 4", "Player 5", "Player 6"],
        #         "scoreTeamA": 30,
        #         "scoreTeamB": 20,
        #         "totalTeamA": 100,
        #         "totalTeamB": 90,
        #         "colourTeamA": "red",
        #         "colourTeamB": "blue"
        #     },
        #     {
        #         "date": "2023-08-16",
        #         "teamA": ["Player 7", "Player 8", "Player 9"],
        #         "teamB": ["Player 10", "Player 11", "Player 12"],
        #         "scoreTeamA": 3,
        #         "scoreTeamB": 2,
        #         "totalTeamA": 50,
        #         "totalTeamB": 45,
        #         "colourTeamA": "green",
        #         "colourTeamB": "yellow"
        #     }
        # ]
        data = response.json()
        context = "Game stats:\n"
        for game in data:
            context += (f"Date: {game['date']}, Team A: {game['teamA']}, Team B: {game['teamB']}, "
                        f"Score Team A: {game['scoreTeamA']}, Score Team B: {game['scoreTeamB']}, "
                        f"Total Team A: {game['totalTeamA']}, Total Team B: {game['totalTeamB']}, "
                        f"Colour Team A: {game['colourTeamA']}, Colour Team B: {game['colourTeamB']}\n")
        return context
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return "Failed to fetch game stats."

def most_recent_game():
    response = requests.get(games_api_url + "/" + "most_recent_game", headers=access_headers)
    if response.status_code == 200:
        #Example output:
        # [{'date': '2023-08-30', 
        # 'teamA': [['Player 1', 
        # 'Player 2', 'Player 3', 
        # 'Player 4', 'Player 5']], 
        # 'teamB': [['Player 6', 
        # 'Player 7', 'Player 8', 
        # 'Player 9', 'Player 10']], 
        # 'scoreTeamA': 30, 
        # 'scoreTeamB': 20, 
        # 'totalTeamA': 100, 
        # 'totalTeamB': 100, 
        # 'colourTeamA': 'red', 
        # 'colourTeamB': 'blue'}]
        data = response.json()
        return data[0] #Output only 1 game
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []


def date():
    list = most_recent_game()["date"]
    return list

def teama():
    list = most_recent_game()["teamA"]
    return list

def teamb():
    list = most_recent_game()["teamB"]
    return list

def scorea():
    list = most_recent_game()["scoreTeamA"]
    return list

def scoreb():
    list = most_recent_game()["scoreTeamB"]
    return list

def totala():
    list = most_recent_game()["totalTeamA"]
    return list

def totalb():
    list = most_recent_game()["totalTeamB"]
    return list

def coloura():
    list = most_recent_game()["colourTeamA"]
    return list

def colourb():
    list = most_recent_game()["colourTeamB"]
    return list


#### TESTS #####
# get_game_stats = game_stats()
# print("Game Stats:", get_game_stats)

# get_date = date()
# print("Date:", get_date)

# get_teama = teama()
# print("TeamA:", get_teama)

# get_teamb = teamb()
# print("TeamB:", get_teamb)

# get_scorea = scorea()
# print("Score Team A:", int(get_scorea))

# get_scoreb = scoreb()
# print("Score Team B:", int(get_scoreb))

# get_totala = totala()
# print("Total Team A:", int(get_totala))

# get_totalb = totalb()
# print("Total Team B:", int(get_totalb))

# get_coloura = coloura()
# print("Colour Team A:", get_coloura)

# get_colourb = colourb()
# print("Colour Team B:", get_colourb)

# get_most_recent_game = most_recent_game()
# print("Most Recent Game:", get_most_recent_game)