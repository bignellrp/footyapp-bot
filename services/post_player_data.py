import requests

player_api_url = "http://localhost:8080/players"
response = requests.get(player_api_url)

def wipe_tally():
    # Prepare the updated data
    updated_data = {"playing": False}

    # Send a PUT request to update all records
    response = requests.put(player_api_url, json=updated_data)

    if response.status_code == 200:
        print("All records updated successfully")
    else:
        print(f"Failed to update records. Status code: {response.status_code}")

def update_tally(available_players):

    # Send a PUT request to update all records
    response = requests.put(player_api_url + '/update_playing', json=available_players)

    if response.status_code == 200:
        print("Tally updated successfully")
    else:
        print(f"Failed to update records. Status code: {response.status_code}")

