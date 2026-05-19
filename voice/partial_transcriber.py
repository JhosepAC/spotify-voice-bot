import tempfile

import soundfile as sf

from faster_whisper import (
    WhisperModel
)


model = WhisperModel(
    "base",

    device="cpu",

    compute_type="int8"
)


def transcribe_partial(
    audio_data,
    sample_rate=16000
):
    """
    Transcribe partial realtime audio.
    """

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    sf.write(
        temp_file.name,
        audio_data,
        sample_rate
    )

    segments, _ = model.transcribe(
        temp_file.name,

        beam_size=2,

        vad_filter=True
    )

    text = ""

    for segment in segments:

        text += (
            segment.text + " "
        )

    return text.strip()