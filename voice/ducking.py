"""Audio ducking: temporarily lower Spotify volume while listening.

Prevents the microphone from capturing music as a voice command.
Restores the previous volume afterwards. All failures are silent
so listening never breaks because of ducking.
"""

from contextlib import contextmanager

from config.settings import DUCKING_ENABLED, DUCKING_LEVEL


@contextmanager
def audio_ducked():
    """Lower Spotify volume during capture, then restore it."""
    if not DUCKING_ENABLED:
        yield
        return

    previous_volume = None
    try:
        from spotify.player import get_current_volume, set_volume

        previous_volume = get_current_volume()
        target = min(previous_volume, DUCKING_LEVEL)
        if target < previous_volume:
            set_volume(target)
    except Exception:
        previous_volume = None

    try:
        yield
    finally:
        if previous_volume is not None:
            try:
                from spotify.player import set_volume

                set_volume(previous_volume)
            except Exception:
                pass
