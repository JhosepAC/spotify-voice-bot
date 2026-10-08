"""NLP regression tests (no microphone, no network).

Run: python tests/test_nlp.py
Uses rule-based fallback (OLLAMA_ENABLED=false) for deterministic results.
"""

import os
import sys
import time

os.environ["OLLAMA_ENABLED"] = "false"
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from nlp.command_builder import build_command
from nlp.local_classifier import score_intent

# (phrase, expected_intent, expected_entities_subset)
CASES = [
    # Core playback paraphrases (Alexa-style variety)
    ("pon Blinding Lights de The Weeknd", "PLAY_TRACK", {"track_name": "blinding lights"}),
    ("ponme Slow Dancing in the Dark de Joji", "PLAY_TRACK", {"artist_name": "joji"}),
    ("pon algo de Shakira", "PLAY_ARTIST", {"artist_name": "shakira"}),
    ("quiero escuchar algo de Bad Bunny", "PLAY_ARTIST", {"artist_name": "bad bunny"}),
    ("pon otra de Karol G", "PLAY_ARTIST", {"artist_name": "karol g"}),
    ("pon musica de queen", "PLAY_ARTIST", {"artist_name": "queen"}),
    ("toca el álbum Thriller de Michael Jackson", "PLAY_ALBUM", {}),
    ("reproduce la playlist de música para estudiar", "PLAY_PLAYLIST", {}),
    ("pon la playlist para estudiar", "PLAY_PLAYLIST", {}),
    # Transport
    ("dale pausa", "PAUSE", {}),
    ("para la música", "PAUSE", {}),
    ("dale play", "RESUME", {}),
    ("continúa", "RESUME", {}),
    ("siguiente canción", "NEXT_TRACK", {}),
    ("pasa esta", "NEXT_TRACK", {}),
    ("la que sigue", "NEXT_TRACK", {}),
    ("vuelve a la anterior", "PREVIOUS_TRACK", {}),
    # Library + volume paraphrases
    ("me gusta esta canción", "LIKE_SONG", {}),
    ("sube el volumen", "VOLUME_UP", {}),
    ("se escucha bajito subele", "VOLUME_UP", {}),
    ("baja un poco el volumen", "VOLUME_DOWN", {}),
    ("muy fuerte bajale", "VOLUME_DOWN", {}),
    ("pon el volumen al 60", "SET_VOLUME", {"volume_level": 60}),
    ("volumen al 30 por favor", "SET_VOLUME", {"volume_level": 30}),
    # Phase 1: information + disambiguation
    ("que esta sonando", "NOW_PLAYING", {}),
    ("quien canta esto", "NOW_PLAYING", {}),
    ("la segunda", "SELECT_INDEX", {"index": 2}),
    ("pon la 3", "SELECT_INDEX", {"index": 3}),
    ("si esa", "CONFIRM_YES", {}),
    ("no esa no", "CONFIRM_NO", {}),
    ("cancela", "CANCEL", {}),
    ("olvida eso", "CANCEL", {}),
    # Phase 3: transport
    ("adelanta 30 segundos", "SEEK_FORWARD", {"seconds": 30}),
    ("avanza un minuto", "SEEK_FORWARD", {}),
    ("retrocede 15 segundos", "SEEK_BACK", {"seconds": 15}),
    ("regresa 20 segundos", "SEEK_BACK", {"seconds": 20}),
    ("desde el principio", "RESTART", {}),
    ("reinicia la cancion", "RESTART", {}),
    ("alterna", "TOGGLE", {}),
    ("salta 3 canciones", "SKIP_N", {"count": 3}),
    ("pasa 2 temas", "SKIP_N", {"count": 2}),
    # Phase 3: modes + queue
    ("pon en aleatorio", "SHUFFLE_ON", {}),
    ("quita el aleatorio", "SHUFFLE_OFF", {}),
    ("aleatorio", "SHUFFLE_TOGGLE", {}),
    ("repite esta cancion", "REPEAT_MODE", {"mode": "track"}),
    ("repite todo", "REPEAT_MODE", {"mode": "context"}),
    ("no repitas", "REPEAT_MODE", {"mode": "off"}),
    ("agrega esta a la cola", "QUEUE_ADD", {}),
    ("pon despacito en la cola", "QUEUE_ADD", {"track_name": "despacito"}),
    ("que hay en la cola", "QUEUE_LIST", {}),
]

# Noisy STT inputs must still resolve (fuzzy robustness)
NOISY_CASES = [
    ("pon algo de shakira", "PLAY_ARTIST"),
    ("subele", "VOLUME_UP"),
    ("que suena", "NOW_PLAYING"),
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

    for phrase, expected_intent in NOISY_CASES:
        result = build_command(phrase)
        ok = result.get("intent") == expected_intent
        print(f"[{'PASS' if ok else 'FAIL'}] noisy {phrase!r} -> {result.get('intent')}")
        failures += 0 if ok else 1

    # Latency gate: local fuzzy path must stay interactive (<100ms mean).
    samples = [p for p, _, _ in CASES[:10]]
    start = time.perf_counter()
    for phrase in samples:
        score_intent(phrase)
    mean_ms = (time.perf_counter() - start) / len(samples) * 1000
    print(f"\nlocal NLU mean: {mean_ms:.1f}ms (gate <100ms)")
    if mean_ms >= 100:
        print("FAIL latency gate")
        failures += 1

    # Fuzzy search unit check (no network).
    from spotify.search import pick_best

    items = [
        {"name": "Blinding Lights", "artists": [{"name": "The Weeknd"}], "uri": "x"},
        {"name": "Blinding", "artists": [{"name": "Someone"}], "uri": "y"},
    ]
    best, _score = pick_best("blain dilait de weeknd", items, "track")
    ok = best is not None and best["uri"] == "x"
    print(f"[{'PASS' if ok else 'FAIL'}] fuzzy search picks right track despite STT noise")
    failures += 0 if ok else 1

    total = len(CASES) + len(NOISY_CASES) + 2
    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
