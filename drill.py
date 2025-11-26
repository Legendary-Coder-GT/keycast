import json
import os
from collections import Counter
from itertools import cycle
from pathlib import Path
from typing import Iterable
from urllib import request, error

from persistence import load_recent_sessions


def load_env_file(path: str | os.PathLike[str] = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        if not line or line.strip().startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        if key and key not in os.environ:
            os.environ[key.strip()] = val.strip().strip('"').strip("'")


def top_error_keys(limit_sessions: int = 10, top_k: int = 8) -> list[str]:
    sessions = load_recent_sessions("data/sessions", limit_sessions)
    counter: Counter[str] = Counter()
    for sess in sessions:
        errors = sess.get("errors", {})
        for key, count in errors.items():
            counter[key] += count
    return [k for k, _ in counter.most_common(top_k)]


def synthesize_drill_text(error_keys: Iterable[str], length: int = 400) -> str:
    """Fallback generator: repeat weak keys in short, vowel-mixed fragments."""
    keys = [k for k in error_keys if k.strip()]
    if not keys:
        return ""
    vowels = "aeiou"
    output = []
    key_cycle = cycle(keys)
    vowel_cycle = cycle(vowels)
    spacer_cycle = cycle([" ", " ", "  "])
    while len("".join(output)) < length:
        key_char = next(key_cycle)
        frag = f"{key_char}{next(vowel_cycle)}{key_char}"
        output.append(frag)
        output.append(next(spacer_cycle))
    return "".join(output)[:length].strip()


def _call_openai(prompt: str, api_key: str, max_tokens: int = 400, model: str = "gpt-4o-mini") -> str | None:
    url = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a typing drill generator. Produce a single practice passage "
                    "that heavily features the provided weak characters, mixes short "
                    "pronounceable pseudo-words and simple real words, keeps everything "
                    "lowercase ASCII, and avoids punctuation beyond spaces."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": max_tokens,
    }
    data = json.dumps(payload).encode()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    req = request.Request(url, data=data, headers=headers)
    try:
        with request.urlopen(req, timeout=25) as resp:
            body = resp.read().decode()
        parsed = json.loads(body)
        return parsed["choices"][0]["message"]["content"].strip()
    except Exception:
        return None


def generate_drill_text(length: int = 400) -> str | None:
    load_env_file()
    sessions = load_recent_sessions("data/sessions", 15)
    errors = top_error_keys()
    if not errors:
        return None

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        summary = []
        total_errors = Counter()
        for sess in sessions:
            for k, v in sess.get("errors", {}).items():
                total_errors[k] += v
        summary.append("Top weak keys with counts: " + ", ".join(f"{k}:{v}" for k, v in total_errors.most_common(10)))
        summary.append(f"Target length ~{length} characters.")
        prompt = "\n".join(summary)
        ai_text = _call_openai(prompt, api_key, max_tokens=600)
        if ai_text:
            # strip leading/trailing whitespace and limit length
            return ai_text.replace("\n", " ").strip()[:length]

    return synthesize_drill_text(errors, length=length)
