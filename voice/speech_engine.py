from faster_whisper import (
    WhisperModel
)

from voice.audio_enhancer import (
    enhance_audio
)


print(
    "Loading Faster Whisper model..."
)


model = WhisperModel(
    "base",

    device="cpu",

    compute_type="int8"
)


def transcribe_audio(audio_path):
    """
    Transcribe microphone audio.
    """

    enhanced_audio = enhance_audio(
        audio_path
    )

    segments, _ = model.transcribe(
        enhanced_audio,

        beam_size=5,

        vad_filter=True
    )

    text = ""

    for segment in segments:

        text += (
            segment.text + " "
        )

    return text.strip()