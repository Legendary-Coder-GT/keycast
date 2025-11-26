import json
import os
from pathlib import Path
from typing import Any, Iterable


def _safe_filename(timestamp: str) -> str:
    # Replace characters that may be awkward in filenames.
    return timestamp.replace(":", "-")


def save_session(path: str | os.PathLike[str], session_dict: dict[str, Any]) -> Path:
    """Persist a single session as a JSON file under the target directory."""
    target_dir = Path(path)
    target_dir.mkdir(parents=True, exist_ok=True)
    ts = session_dict.get("timestamp", "session")
    filename = f"session_{_safe_filename(ts)}.json"
    file_path = target_dir / filename
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(session_dict, f, indent=2)
    return file_path


def load_recent_sessions(path: str | os.PathLike[str], limit: int = 10) -> list[dict[str, Any]]:
    """Load the most recent session JSON files from a directory."""
    target_dir = Path(path)
    if not target_dir.exists():
        return []

    json_files: Iterable[Path] = sorted(
        (p for p in target_dir.glob("session_*.json") if p.is_file()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    sessions: list[dict[str, Any]] = []
    for file_path in json_files:
        try:
            with file_path.open("r", encoding="utf-8") as f:
                sessions.append(json.load(f))
        except Exception:
            continue
        if len(sessions) >= limit:
            break
    return sessions
