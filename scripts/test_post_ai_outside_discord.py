#!/usr/bin/env python3
"""Run the bot's Gemini call path *without Discord*.

This exercises services/post_ai.py exactly as the bot does (including:
- reading GOOGLE_API_KEY / GEMINI_MODEL from env/.env
- rate limiting
- token/output caps
- caching

Examples:
  ./.venv/bin/python scripts/test_post_ai_outside_discord.py \
    --query "Who is top scorer?" \
    --context "Player1: W10 D5 L3 ..."

  ./.venv/bin/python scripts/test_post_ai_outside_discord.py \
    --query "Summarise the stats" \
    --context-file sample_context.txt

  # Burst test (should throttle politely)
  ./.venv/bin/python scripts/test_post_ai_outside_discord.py --burst 5
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.post_ai import get_ai_response


DEFAULT_CONTEXT = (
    "Player stats (example):\n"
    "- Alice: W10 D2 L1 (Top scorer)\n"
    "- Bob:   W5  D3 L6\n\n"
    "Game stats (example):\n"
    "- Last game: Alice 3 goals, Bob 1 goal\n"
)


async def _run_once(query: str, context: str) -> str:
    return await get_ai_response(query, context)


def main() -> int:
    parser = argparse.ArgumentParser(description="Test services.post_ai.get_ai_response outside Discord")
    parser.add_argument("--env", default=".env", help="Path to .env file (default: .env)")
    parser.add_argument("--query", default="Who is the top scorer?", help="User query to send")
    parser.add_argument("--context", default=None, help="Context string to send")
    parser.add_argument("--context-file", default=None, help="Load context from a file")
    parser.add_argument("--burst", type=int, default=1, help="Run N requests sequentially (default: 1)")
    args = parser.parse_args()

    # Load .env so you can run this without exporting variables.
    if args.env:
        load_dotenv(args.env)

    context = DEFAULT_CONTEXT
    if args.context_file:
        context = Path(args.context_file).read_text(encoding="utf-8")
    elif args.context is not None:
        context = args.context

    burst = max(1, int(args.burst))
    for i in range(burst):
        if burst > 1:
            print(f"\n--- Request {i+1}/{burst} ---")
        response = asyncio.run(_run_once(args.query, context))
        print(response)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
