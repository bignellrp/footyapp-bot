from dotenv import load_dotenv
import google.generativeai as genai
from services.get_player_data import *
import os

load_dotenv()  # Load environment variables from .env

GOOGLE_TOKEN = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_TOKEN)

# Use the correct model name for the stable API
try:
    model = genai.GenerativeModel("gemini-pro")
except Exception as e:
    print(f"Failed to initialize gemini-pro, trying fallback: {e}")
    # Fallback to text-bison if gemini-pro fails
    model = genai.GenerativeModel("text-bison-001")

def get_ai_response(query, context):
    prompt = f"{context}\n\nUser query: {query}\n\nNote: Only answer questions related to the provided football player stats. If the question is unrelated, respond with 'I'm only here to answer questions about football stats'"
    
    try:
        response = model.generate_content(prompt)
        ai_response = response.text
    except Exception as e:
        print(f"AI API Error: {e}")
        return "Sorry, I'm having trouble connecting to the AI service right now. Please try again later."

    if len(ai_response) > 2000:
        ai_response = ai_response[:1997] + "..."

    return ai_response