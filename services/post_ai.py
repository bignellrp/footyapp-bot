from dotenv import load_dotenv, dotenv_values
import google.generativeai as genai
from services.get_player_data import *

load_dotenv()  # Load environment variables from .env
config = dotenv_values(".env")

GOOGLE_TOKEN = config["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_TOKEN)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_ai_response(query, context):
    response = model.generate_content(f"{context}\n\nUser query: {query}")
    return response.text

def format_stats_for_context(stats):
    context = "Player stats:\n"
    for player in stats:
        context += f"Name: {player[0]}, Wins: {player[1]}, Draws: {player[2]}, Losses: {player[3]}, Score: {player[4]}, Win Percentage: {player[5]}\n"
    return context