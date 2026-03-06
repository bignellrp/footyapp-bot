# footyapp-bot
Footyapp Frontend for Discord Bot

## Setup

### 1) Discord bot token

Create a Discord application + bot, invite it to your server, then set these environment variables.

### 2) Gemini API key (Google AI Studio)

This bot uses the Gemini API via a **Google AI Studio** API key (not a service account).

1. Go to Google AI Studio → **API keys**
2. Create an API key (you’ll see it listed under “Generative Language API Key”)
3. Put it in your `.env` as `GOOGLE_API_KEY`

## Environment variables

Create a `.env` file (do not commit it) containing at least:

```dotenv
# Discord
DISCORD_TOKEN=...your discord bot token...
COMMAND_PREFIX=!

# Gemini (Google AI Studio)
GOOGLE_API_KEY=...your ai studio key...

# Optional: choose the model (default is a cheap/fast “flash” model)
GEMINI_MODEL=gemini-flash-latest
```

Optional “free-tier friendly” tuning (rate limit + caps):

```dotenv
# Global RPM limit inside this bot process (conservative default is 10)
GEMINI_MAX_RPM=10

# Token/output limits
GEMINI_MAX_OUTPUT_TOKENS=256
GEMINI_TEMPERATURE=0.2

# Context truncation and caching
GEMINI_MAX_CONTEXT_CHARS=12000
GEMINI_CACHE_TTL_SECONDS=120
GEMINI_CACHE_MAX_ITEMS=200
```

## Run locally

```bash
python3.9 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python bot.py
```

## Test the Gemini key (CLI)

These scripts let you validate the key and the bot’s AI pipeline without Discord.

```bash
./.venv/bin/python scripts/test_google_api_key.py
./.venv/bin/python scripts/test_google_api_key.py --list-models
```

Test the bot’s `services/post_ai.py` path (rate limiting, caching, model fallback, etc.):

```bash
./.venv/bin/python scripts/test_post_ai_outside_discord.py --query "Who is the top scorer?"
./.venv/bin/python scripts/test_post_ai_outside_discord.py --burst 5
```

## Using the AI command in Discord

In Discord, use:

```text
<COMMAND_PREFIX>ai <your question>
```

Example:

```text
!ai Who is the top scorer?
```

Notes:
- The AI command is designed to answer **only** based on the bot’s football stats context.
- If you ask unrelated questions, it should refuse and ask you to keep it football/stats related.


