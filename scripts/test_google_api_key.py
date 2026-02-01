#!/usr/bin/env python3
"""Validate GOOGLE_API_KEY from a .env file against the Gemini API.

What it does:
- Loads GOOGLE_API_KEY from a specified .env file (default: .env)
- Lists a few available models that support generateContent
- Runs a tiny "hello world" generation call

Usage:
  python3 scripts/test_google_api_key.py
  python3 scripts/test_google_api_key.py --env /path/to/.env
  python3 scripts/test_google_api_key.py --model gemini-1.5-flash

Exit codes:
  0 = success
  2 = missing/empty key
  3 = API call failed
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Iterable, Optional

from dotenv import dotenv_values
from google import genai


def _mask_secret(value: str, keep: int = 4) -> str:
    value = value.strip()
    if not value:
        return "<empty>"
    if len(value) <= keep * 2:
        return value[0:keep] + "…"
    return value[:keep] + "…" + value[-keep:]


def _load_google_api_key(env_path: str) -> Optional[str]:
    # Prefer reading directly from the env file so this works even when the user
    # hasn't exported the variable.
    values = dotenv_values(env_path)
    key = values.get("GOOGLE_API_KEY")

    # Fallback to process environment if not present in file.
    if not key:
        key = os.getenv("GOOGLE_API_KEY")

    if key is None:
        return None

    key = str(key).strip()
    return key or None


def _candidate_model_names(model: str) -> list[str]:
    model = (model or "").strip()
    if not model:
        return []
    if model.startswith("models/"):
        return [model]
    return [model, f"models/{model}"]


def _extract_text(response) -> str:
    """Best-effort extraction of text from google-genai responses."""
    text = (getattr(response, "text", None) or "").strip()
    if text:
        return text

    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", None) or []
        for part in parts:
            part_text = (getattr(part, "text", None) or "").strip()
            if part_text:
                return part_text

    # Fall back to a string representation so the user sees *something*.
    return str(response).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Test GOOGLE_API_KEY via Gemini API")
    parser.add_argument("--env", default=".env", help="Path to .env file (default: .env)")
    parser.add_argument(
        "--model",
        default=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        help="Model to test (default: GEMINI_MODEL or gemini-1.5-flash)",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List models supporting generateContent",
    )
    args = parser.parse_args()

    api_key = _load_google_api_key(args.env)
    if not api_key:
        print(f"ERROR: GOOGLE_API_KEY not found in {args.env!r} and not set in the environment.")
        return 2

    print(f"Loaded GOOGLE_API_KEY: {_mask_secret(api_key)}")
    print(f"Testing model: {args.model}")

    try:
        client = genai.Client(api_key=api_key)

        if args.list_models:
            print("\nModels supporting generateContent (first 20):")
            count = 0
            for model in client.models.list():
                actions = getattr(model, "supported_actions", None) or []
                if any(a.lower() in {"generatecontent", "generate_content"} for a in actions):
                    print(f"- {model.name}")
                    count += 1
                    if count >= 20:
                        break
            if count == 0:
                print("(none returned)")

        prompt = "What is the capital of France? Answer with a single word."

        preferred_model = args.model
        fallback_models: list[str] = [
            preferred_model,
            # Common/default model aliases people use.
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-pro",
            "gemini-pro-latest",
            "gemini-flash-latest",
            "models/gemini-2.0-flash",
            "models/gemini-1.5-flash",
        ]

        last_error: Optional[Exception] = None
        used_model: Optional[str] = None
        response = None

        for m in fallback_models:
            for candidate in _candidate_model_names(m):
                try:
                    response = client.models.generate_content(model=candidate, contents=prompt)
                    used_model = candidate
                    break
                except Exception as exc:
                    last_error = exc
            if response is not None:
                break

        if response is None:
            raise RuntimeError("All model attempts failed") from last_error

        text = _extract_text(response)
        print("\nGeneration response:")
        print(text if text else "<empty response>")

        if used_model:
            print(f"\nUsed model: {used_model}")

        normalized = " ".join((text or "").strip().split()).lower()
        expected = "paris"

        print("\nResponse analysis:")
        if not normalized:
            print("- Empty response")
        else:
            print(f"- Normalized: {normalized!r}")
            print(f"- Contains expected '{expected}': {expected in normalized}")

        if normalized and normalized != expected and expected not in normalized:
            print("\nNOTE: Unexpected answer for this prompt; key may still be valid.")

        print("\nOK: Gemini API key appears to be working.")
        return 0

    except Exception as exc:
        print("\nERROR: Gemini API call failed.")
        print(f"Type: {type(exc).__name__}")
        print(f"Message: {exc}")
        print(
            "\nCommon causes:\n"
            "- Wrong key or key disabled\n"
            "- Key restrictions (IP/HTTP referrer) blocking the host where this runs\n"
            "- Billing/quota issues\n"
            "- Model name not available for your project/region\n"
            "\nNext steps:\n"
            "- Re-run with: --list-models\n"
            "- If using Docker, run this inside the container (same network/IP)\n"
        )
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
