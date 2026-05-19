import webrtcvad


vad = webrtcvad.Vad(3)


def detect_voice(
    audio_bytes,
    sample_rate=16000
):
    """
    Detect human voice.
    """

    try:

        return vad.is_speech(
            audio_bytes,
            sample_rate
        )

    except Exception:

        return False