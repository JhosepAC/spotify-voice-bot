"""Phase 3 regression tests: full Spotify matrix offline via FakeSpotify.

Run: python tests/test_phase3.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tests.fake_spotify import FakeSpotify

import spotify.player as player
import spotify.device as device
import spotify.like as like

FAKE = FakeSpotify()


def use_fake():
    player._sp = lambda: FAKE
    device._sp = lambda: FAKE
    like._sp = lambda: FAKE
    FAKE.calls.clear()


def test_seek_forward_moves_position():
    use_fake()
    from commands.handlers import handle_seek_forward

    msg = handle_seek_forward(30)
    seeks = FAKE.called("seek_track")
    assert seeks and seeks[0][1] == 90000, seeks
    assert "30" in msg, msg


def test_seek_back_defaults_and_clamps():
    use_fake()
    from commands.handlers import handle_seek_back

    FAKE.playback["progress_ms"] = 5000
    msg = handle_seek_back(None)
    seeks = FAKE.called("seek_track")
    assert seeks and seeks[-1][1] == 0, seeks
    assert "15" in msg, msg
    FAKE.playback["progress_ms"] = 60000


def test_restart_goes_to_zero():
    use_fake()
    from commands.handlers import handle_restart

    assert "principio" in handle_restart().lower()
    assert FAKE.called("seek_track")[-1][1] == 0


def test_toggle_pauses_and_resumes():
    use_fake()
    from commands.handlers import handle_toggle

    FAKE.playback["is_playing"] = True
    assert "paus" in handle_toggle().lower()
    assert FAKE.called("pause_playback")
    assert "sigamos" in handle_toggle().lower()
    assert FAKE.called("start_playback")


def test_skip_n_advances_n_tracks():
    use_fake()
    from commands.router import route_command

    msg = route_command("SKIP_N", {"count": 3})
    assert len(FAKE.called("next_track")) == 3
    assert "3" in msg, msg


def test_router_transport_wiring():
    use_fake()
    from commands.router import route_command

    assert "30" in route_command("SEEK_FORWARD", {"seconds": 30})
    assert "principio" in route_command("RESTART", {}).lower()


def main() -> int:
    tests = [
        test_seek_forward_moves_position,
        test_seek_back_defaults_and_clamps,
        test_restart_goes_to_zero,
        test_toggle_pauses_and_resumes,
        test_skip_n_advances_n_tracks,
        test_router_transport_wiring,
    ]
    failures = 0
    for fn in tests:
        try:
            fn()
            print(f"[PASS] {fn.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"[FAIL] {fn.__name__}: {e}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
