"""NLP regression tests (no microphone, no network).

Run: python tests/test_nlp.py
Uses rule-based fallback (OLLAMA_ENABLED=false) for deterministic results.
"""

import os
import sys

os.environ["OLLAMA_ENABLED"] = "false"
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from nlp.command_builder import build_command

# (phrase, expected_intent, expected_entities_subset)
CASES = [
    ("pon Blinding Lights de The Weeknd", "PLAY_TRACK", {"track_name": "blinding lights"}),
    ("ponme Slow Dancing in the Dark de Joji", "PLAY_TRACK", {"artist_name": "joji"}),
    ("pon algo de Shakira", "PLAY_ARTIST", {"artist_name": "shakira"}),
    ("quiero escuchar algo de Bad Bunny", "PLAY_ARTIST", {"artist_name": "bad bunny"}),
    ("pon otra de Karol G", "PLAY_ARTIST", {"artist_name": "karol g"}),
    ("toca el álbum Thriller de Michael Jackson", "PLAY_ALBUM", {}),
    ("reproduce la playlist de música para estudiar", "PLAY_PLAYLIST", {}),
    ("dale pausa", "PAUSE", {}),
    ("para la música", "PAUSE", {}),
    ("dale play", "RESUME", {}),
    ("continúa", "RESUME", {}),
    ("siguiente canción", "NEXT_TRACK", {}),
    ("pasa esta", "NEXT_TRACK", {}),
    ("vuelve a la anterior", "PREVIOUS_TRACK", {}),
    ("me gusta esta canción", "LIKE_SONG", {}),
    ("sube el volumen", "VOLUME_UP", {}),
    ("baja un poco el volumen", "VOLUME_DOWN", {}),
    ("pon el volumen al 60", "SET_VOLUME", {"volume_level": 60}),
    ("volumen al 30 por favor", "SET_VOLUME", {"volume_level": 30}),
]


def main() -> int:
    failures = 0
    for phrase, expected_intent, expected_entities in CASES:
        result = build_command(phrase)
        intent = result.get("intent")
        entities = result.get("entities", {})
        ok = intent == expected_intent and all(
            entities.get(k) == v for k, v in expected_entities.items()
        )
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {phrase!r} -> {intent} {entities}")
        if not ok:
            print(f"   expected: {expected_intent} {expected_entities}")
            failures += 1
    print(f"\n{len(CASES) - failures}/{len(CASES)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
