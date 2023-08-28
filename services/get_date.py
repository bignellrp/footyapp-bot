import datetime
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get gameday from .env file
INPUT_GAMEDAY = os.getenv("GAMEDAY")

# Convert weekday name to a number (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
weekday_number = datetime.strptime(INPUT_GAMEDAY, "%A").weekday()

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + timedelta(days_ahead)

d = datetime.today()
# Games are played on {INPUT_GAMEDAY}, so return next {INPUT_GAMEDAY} date
weekday = next_weekday(d, 2)
gameday = weekday.strftime('%Y-%m-%d')