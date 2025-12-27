#!/usr/bin/env python3
"""
Quick script to check available Google AI models
Run this to see what models you can actually use
"""

from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
GOOGLE_TOKEN = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_TOKEN)

print("Available models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")