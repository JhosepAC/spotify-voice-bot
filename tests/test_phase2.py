"""Phase 2 regression tests (no microphone, no network, no credentials).

Run: python tests/test_phase2.py
Spotify/TTS hardware is stubbed out.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import context.state as state
from context.manager import get_last_candidates, clear_candidates
from voice.tts import _chunks


def _reset():
    clear_candidates()
    state.LAST_TRACK = None
    state.LAST_ARTIST = None


def test_chunks_split():
    chunks = _chunks("Reproduciendo Blinding Lights de The Weeknd. Di sí o la segunda.")
    assert len(chunks) == 2, chunks
    assert all(c for c in chunks)


def test_low_score_asks_instead_of_playing():
    import commands.handlers as handlers

    _reset()
    calls = []
    handlers.preview_candidates = lambda q, t="track": {
        "label": "Blinding Lights de The Weeknd",
        "score": 52.0,
        "candidates": [
            {"uri": "u1", "label": "Blinding Lights de The Weeknd", "search_type": "track"},
            {"uri": "u2", "label": "Blinding de Someone", "search_type": "track"},
        ],
    }
    handlers.resolve_and_play = lambda q, search_type="track": calls.append(q) or {
        "success": True, "label": "X", "score": 99.0, "candidates": []
    }

    msg = handlers.handle_play_track("blain dilait", "weeknd")
    assert "sí" in msg.lower() or "segunda" in msg.lower(), msg
    assert calls == [], "must not play on low confidence"
    assert len(get_last_candidates()) == 2


def test_confirm_yes_plays_first_candidate():
    import commands.router as router

    _reset()
    played = []
    router.play_candidate = lambda uri, st="track": played.append(uri) or True
    state.LAST_CANDIDATES = [
        {"uri": "u1", "label": "First", "search_type": "track"},
        {"uri": "u2", "label": "Second", "search_type": "track"},
    ]
    msg = router.route_command("CONFIRM_YES", {})
    assert played == ["u1"], played
    assert "First" in msg, msg


def test_select_index_plays_second_candidate():
    import commands.router as router

    _reset()
    played = []
    router.play_candidate = lambda uri, st="track": played.append(uri) or True
    state.LAST_CANDIDATES = [
        {"uri": "u1", "label": "First", "search_type": "track"},
        {"uri": "u2", "label": "Second", "search_type": "track"},
    ]
    msg = router.route_command("SELECT_INDEX", {"index": 2})
    assert played == ["u2"], played
    assert "Second" in msg, msg


def test_select_without_candidates_guides_user():
    import commands.router as router

    _reset()
    msg = router.route_command("SELECT_INDEX", {"index": 2})
    assert "primero" in msg.lower() or "opciones" in msg.lower(), msg


def test_wake_disabled_is_instant_passthrough():
    from voice.wake import wait_for_wake

    assert wait_for_wake() is True


def main() -> int:
    tests = [
        test_chunks_split,
        test_low_score_asks_instead_of_playing,
        test_confirm_yes_plays_first_candidate,
        test_select_index_plays_second_candidate,
        test_select_without_candidates_guides_user,
        test_wake_disabled_is_instant_passthrough,
    ]
    failures = 0
    for fn in tests:
        try:
            fn()
            print(f"[PASS] {fn.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"[FAIL] {fn.__name__}: {e}")
        finally:
            _reset()
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
