import requests
from services.get_date import gameday
import json
from dotenv import load_dotenv
import os
from services.post_player_data import *

##Load the .env file
load_dotenv()

# Login to the API to get JWT token
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")

# Url used for login
login_api_url = "http://localhost:8080/login"

response = requests.post(login_api_url, json={"username": API_USERNAME, "password": API_PASSWORD})
access_token = response.json()["access_token"]
access_headers = {
    "Authorization": f"Bearer {access_token}"
}

# Url used for games data
games_api_url = "http://localhost:8080/games"

def update_result(game_data):
    '''Update the result of a game that already exists in the database'''
    # Send a PUT request to update all records
    # Example json game_data =
    # {
    # "date": "2023-08-15",
    # "teamA": [
    #     "Player 1",
    #     "Player 2",
    #     "Player 3",
    #     "Player 4",
    #     "Player 5"
    # ],
    # "teamB": [
    #     "Player 6",
    #     "Player 7",
    #     "Player 8",
    #     "Player 9",
    #     "Player 10"
    # ],
    # "scoreTeamA": 3,
    # "scoreTeamB": 2,
    # "totalTeamA": 100,
    # "totalTeamB": 100,
    # "colourTeamA": "red",
    # "colourTeamB": "blue"
    # }
    response = requests.put(games_api_url + "/" + game_data["date"], json=game_data, headers=access_headers)

    if response.status_code == 200:
        print("Game updated successfully")
        wipe_tally()
    else:
        print(f"Failed to update record. Status code: {response.status_code}")

def append_result(game_data):
    '''Add a new game to the database'''
    # Send a POST request to update all records
    # Example json game_data =
    # {
    # "date": "2023-08-15",
    # "teamA": [
    #     "Player 1",
    #     "Player 2",
    #     "Player 3",
    #     "Player 4",
    #     "Player 5"
    # ],
    # "teamB": [
    #     "Player 6",
    #     "Player 7",
    #     "Player 8",
    #     "Player 9",
    #     "Player 10"
    # ],
    # "scoreTeamA": 3,
    # "scoreTeamB": 2,
    # "totalTeamA": 100,
    # "totalTeamB": 100,
    # "colourTeamA": "red",
    # "colourTeamB": "blue"
    # }
    response = requests.post(games_api_url, json=game_data, headers=access_headers)

    if response.status_code == 200:
        print("Game added successfully")
        wipe_tally()
    else:
        print(f"Failed to add record. Status code: {response.status_code}")

def update_score_result(score):
    '''Update the result of a game that already exists in the database
    based on the score the stats are also updated by the API'''
    # Send a PUT request to update all records
    # Example json score =
    # {
    # "scoreTeamA": 5,
    # "scoreTeamB": 4
    # }
    date = gameday
    response = requests.put(games_api_url + "/updatescore/" + date, json=score, headers=access_headers)

    if response.status_code == 200:
        print("Game updated successfully")
        wipe_tally()
    else:
        print(f"Failed to update record. Status code: {response.status_code}")

def swap_players(current_player, new_player):
    '''Swap players in the most recent game and update totals'''
    # Example usage
    # current_player = "PlayerA"
    # new_player = "PlayerB"
    # swap_players(current_player, new_player)
    payload = {
        "current_player": current_player,
        "new_player": new_player
    }
    
    response = requests.put(games_api_url + "/swap_player", json=payload, headers=access_headers)

    if response.status_code == 200:
        print("Players swapped and totals updated successfully")
    else:
        print(f"Failed to swap players. Status code: {response.status_code}")

##### TESTS #####

# current_player = "Cla"
# new_player = "Emily"
# swap_players(current_player, new_player)