import numpy as np

from voice.audio_config import (
    SILENCE_THRESHOLD
)


def is_speech(audio_chunk):
    """
    Detect if chunk contains speech.
    """

    energy = np.linalg.norm(
        audio_chunk
    )

    return energy > SILENCE_THRESHOLD