import numpy as np


def normalize_audio(audio):
    """
    Normalize audio volume.
    """

    max_value = np.max(
        np.abs(audio)
    )

    if max_value == 0:
        return audio

    return audio / max_value


def remove_noise(audio):
    """
    Basic noise reduction.
    """

    noise_floor = 0.01

    cleaned = np.where(

        np.abs(audio) < noise_floor,

        0,

        audio
    )

    return cleaned