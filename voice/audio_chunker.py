import numpy as np


def chunk_to_bytes(chunk):
    """
    Convert chunk to bytes.
    """

    audio_int16 = (

        chunk * 32767

    ).astype(np.int16)

    return audio_int16.tobytes()