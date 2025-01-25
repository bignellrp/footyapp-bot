from dotenv import load_dotenv
import google.generativeai as genai
from services.get_player_data import *
import os

load_dotenv()  # Load environment variables from .env

GOOGLE_TOKEN = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_TOKEN)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_ai_response(query, context):
    prompt = f"{context}\n\nUser query: {query}\n\nNote: Only answer questions related to the provided football player stats. If the question is unrelated, respond with 'I'm only here to answer questions about football stats'"
    response = model.generate_content(prompt)
    ai_response = response.text

    if len(ai_response) > 2000:
        ai_response = ai_response[:1997] + "..."

    return ai_response