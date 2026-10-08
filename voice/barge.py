"""Barge-in lite: let the user interrupt a spoken reply.

Samples short microphone windows while TTS plays and reports an
interruption when input stays clearly above the noise floor.

Disabled by default (BARGE_IN_ENABLED=false): without acoustic echo
cancellation the speakers alone can trigger it. Enable with headphones
or a directional mic.
"""

import time

import numpy as np
import sounddevice as sd

from config.settings import (
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
    BASE_ENERGY_THRESHOLD,
    BARGE_IN_ENABLED,
    BARGE_IN_RATIO,
)


def sample_rms(seconds: float = 0.15) -> float:
    """Record a short window and return its RMS energy."""
    frames = int(AUDIO_SAMPLE_RATE * seconds)
    try:
        with sd.InputStream(
            samplerate=AUDIO_SAMPLE_RATE,
            channels=AUDIO_CHANNELS,
            dtype="float32",
            blocksize=1024,
        ) as stream:
            chunk, _ = stream.read(frames)
        return float(np.sqrt(np.mean(np.asarray(chunk, dtype=np.float32) ** 2)))
    except Exception:
        return 0.0


def make_abort_checker(grace_seconds: float = 1.0):
    """
    Build a should_abort() callback for TTS.

    Ignores the grace window (TTS onset) and then aborts when mic
    energy clearly exceeds the ambient floor.
    """
    start = time.perf_counter()
    threshold = max(BASE_ENERGY_THRESHOLD * BARGE_IN_RATIO, 0.02)

    def should_abort() -> bool:
        if not BARGE_IN_ENABLED:
            return False
        if time.perf_counter() - start < grace_seconds:
            return False
        return sample_rms() > threshold

    return should_abort
