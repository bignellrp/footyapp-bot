import requests

games_api_url = "http://localhost:8080/games"
response = requests.get(games_api_url)

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
    response = requests.put(games_api_url + game_data["date"], json=game_data)

    if response.status_code == 200:
        print("Game updated successfully")
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
    response = requests.post(games_api_url, json=game_data)

    if response.status_code == 200:
        print("Game added successfully")
    else:
        print(f"Failed to add record. Status code: {response.status_code}")

def update_score_result(date,score):
    '''Update the result of a game that already exists in the database'''
    # Send a PUT request to update all records
    # Example json score =
    # {
    # "scoreTeamA": 5,
    # "scoreTeamB": 4
    # }
    response = requests.put(games_api_url + date, json=score)

    if response.status_code == 200:
        print("Game updated successfully")
    else:
        print(f"Failed to update record. Status code: {response.status_code}")


date = "2023-08-15"
score = {
    "scoreTeamA": 5,
    "scoreTeamB": 4
}
update_score_result(date,score)

game_data = [
    {
    "date": "2023-08-15",
    "teamA": [
        "Player 1",
        "Player 2",
        "Player 3",
        "Player 4",
        "Player 5"
    ],
    "teamB": [
        "Player 6",
        "Player 7",
        "Player 8",
        "Player 9",
        "Player 10"
    ],
    "scoreTeamA": 3,
    "scoreTeamB": 2,
    "totalTeamA": 100,
    "totalTeamB": 100,
    "colourTeamA": "red",
    "colourTeamB": "blue"
    }
]

update_result(game_data)

new_game_data = [
    {
    "date": "2023-08-16",
    "teamA": [
        "Player 1",
        "Player 2",
        "Player 3",
        "Player 4",
        "Player 5"
    ],
    "teamB": [
        "Player 6",
        "Player 7",
        "Player 8",
        "Player 9",
        "Player 10"
    ],
    "scoreTeamA": 3,
    "scoreTeamB": 2,
    "totalTeamA": 100,
    "totalTeamB": 100,
    "colourTeamA": "red",
    "colourTeamB": "blue"
    }
]

append_result(new_game_data)