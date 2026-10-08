"""Turn telemetry: JSONL logs plus optional audio snapshots.

Every voice turn appends one line to logs/turns.jsonl with text,
intent, entities and per-stage latencies. Raw microphone audio can
be saved to temp/ for debugging STT issues.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from config.settings import LOGS_DIR, TEMP_DIR

TURNS_FILE = LOGS_DIR / "turns.jsonl"


def log_turn(record: dict) -> None:
    """Append one turn record (never raises)."""
    try:
        entry = {"ts": datetime.now(timezone.utc).isoformat(), **record}
        TURNS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TURNS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


def save_audio_snapshot(audio, sample_rate: int, prefix: str = "cmd") -> str | None:
    """Save a mono float32 array to temp/ as WAV. Returns path or None."""
    try:
        import soundfile as sf

        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        millis = int((time.time() % 1) * 1000)
        path: Path = TEMP_DIR / f"{prefix}-{stamp}-{millis:03d}.wav"
        path.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(path), audio, sample_rate)
        return str(path)
    except Exception:
        return None
