from dotenv import load_dotenv
from google import genai
from services.get_player_data import *
import logging
import os
import asyncio
import time
from collections import deque
from hashlib import sha256

logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env (optional when running via docker-compose env_file)

GOOGLE_TOKEN = os.getenv("GOOGLE_API_KEY")

_client = None

_rate_lock = None
_rate_lock_loop = None
_request_timestamps = deque()

_cache = {}


def _get_client():
    global _client

    if _client is not None:
        return _client

    if not GOOGLE_TOKEN:
        raise RuntimeError("Missing GOOGLE_API_KEY environment variable")

    _client = genai.Client(api_key=GOOGLE_TOKEN)
    return _client


def _get_rate_lock():
    global _rate_lock, _rate_lock_loop

    loop = asyncio.get_running_loop()
    if _rate_lock is None or _rate_lock_loop is not loop:
        _rate_lock = asyncio.Lock()
        _rate_lock_loop = loop
    return _rate_lock


def _candidate_model_names(model: str):
    model = (model or "").strip()
    if not model:
        return []
    if model.startswith("models/"):
        return [model]
    return [model, f"models/{model}"]


async def _enforce_rate_limit():
    """Global per-process RPM limiter.

    This is intentionally conservative by default to reduce the chance of hitting
    free-tier rate limits.
    """

    max_rpm = int(os.getenv("GEMINI_MAX_RPM", "10"))
    if max_rpm <= 0:
        return

    window_s = float(os.getenv("GEMINI_RPM_WINDOW_SECONDS", "60"))
    if window_s <= 0:
        return

    lock = _get_rate_lock()
    async with lock:
        now = time.monotonic()
        cutoff = now - window_s
        while _request_timestamps and _request_timestamps[0] < cutoff:
            _request_timestamps.popleft()

        if len(_request_timestamps) < max_rpm:
            _request_timestamps.append(now)
            return

        # Need to wait until the earliest timestamp expires.
        earliest = _request_timestamps[0]
        wait_s = max(0.0, (earliest + window_s) - now)

    # Sleep outside the lock so other coroutines can progress.
    if wait_s > 0:
        await asyncio.sleep(wait_s)
    await _enforce_rate_limit()


def _cache_get(key: str):
    ttl_s = int(os.getenv("GEMINI_CACHE_TTL_SECONDS", "120"))
    if ttl_s <= 0:
        return None

    item = _cache.get(key)
    if not item:
        return None

    expires_at, value = item
    if time.monotonic() >= expires_at:
        _cache.pop(key, None)
        return None
    return value


def _cache_set(key: str, value: str):
    ttl_s = int(os.getenv("GEMINI_CACHE_TTL_SECONDS", "120"))
    if ttl_s <= 0:
        return

    max_items = int(os.getenv("GEMINI_CACHE_MAX_ITEMS", "200"))
    if max_items > 0 and len(_cache) >= max_items:
        # Simple eviction: drop an arbitrary item.
        _cache.pop(next(iter(_cache)))

    _cache[key] = (time.monotonic() + ttl_s, value)


async def get_ai_response(query, context):
    max_context_chars = int(os.getenv("GEMINI_MAX_CONTEXT_CHARS", "12000"))
    if max_context_chars > 0 and context and len(context) > max_context_chars:
        context = context[-max_context_chars:]

    prompt = f"{context}\n\nUser query: {query}\n\nNote: Only answer questions related to the provided football player stats. If the question is unrelated, respond with 'I'm only here to answer questions about football stats'"

    cache_key = sha256(prompt.encode("utf-8")).hexdigest()
    cached = _cache_get(cache_key)
    if cached:
        return cached
    
    try:
        client = _get_client()

        # Prefer an inexpensive, widely-available model for free tier.
        preferred_model = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
        # Keep a pragmatic fallback list in case the preferred model isn't enabled.
        fallback_models = [
            preferred_model,
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-flash-latest",
            "gemini-pro-latest",
            "gemini-pro",
        ]

        max_output_tokens = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "256"))
        temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.2"))
        config = {
            "max_output_tokens": max_output_tokens,
            "temperature": temperature,
        }

        await _enforce_rate_limit()

        last_error = None
        ai_response = None
        for model_name in fallback_models:
            for candidate in _candidate_model_names(model_name):
                try:
                    response = await asyncio.to_thread(
                        client.models.generate_content,
                        model=candidate,
                        contents=prompt,
                        config=config,
                    )

                    ai_response = (getattr(response, "text", None) or "").strip() or None
                    if ai_response is None:
                        ai_response = str(response)
                    break
                except Exception as exc:
                    last_error = exc
                    logger.warning("Failed to generate with model %s", candidate, exc_info=True)
            if ai_response is not None:
                break

        if ai_response is None:
            raise RuntimeError("Failed to generate content with any Gemini model") from last_error
    except Exception as e:
        logger.exception("AI API Error")
        if "Missing GOOGLE_API_KEY" in str(e):
            return "AI is not configured on this bot (missing GOOGLE_API_KEY)."
        return "Sorry, I'm having trouble connecting to the AI service right now. Please try again later."

    if len(ai_response) > 2000:
        ai_response = ai_response[:1997] + "..."

    _cache_set(cache_key, ai_response)
    return ai_response