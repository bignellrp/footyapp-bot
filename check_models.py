#!/usr/bin/env python3
"""
Quick script to check available Google AI models
Run this to see what models you can actually use
"""

from dotenv import load_dotenv
from google import genai
import os

def main() -> None:
    load_dotenv()
    google_token = os.getenv("GOOGLE_API_KEY")

    if not google_token:
        raise RuntimeError("Missing GOOGLE_API_KEY environment variable")

    client = genai.Client(api_key=google_token)

    print("Available models:")
    for model in client.models.list():
        actions = getattr(model, "supported_actions", None) or []
        if any(a.lower() in {"generatecontent", "generate_content"} for a in actions):
            print(f"- {model.name}")


if __name__ == "__main__":
    main()