import webrtcvad


vad = webrtcvad.Vad(2)


def is_speech(audio_bytes, sample_rate=16000):
    """
    Detect speech.
    """

    return vad.is_speech(
        audio_bytes,
        sample_rate
    )