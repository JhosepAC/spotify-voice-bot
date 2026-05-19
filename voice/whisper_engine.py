import tempfile

import soundfile as sf

from faster_whisper import (
    WhisperModel
)


print(
    "Loading Faster-Whisper model..."
)

model = WhisperModel(

    "medium",

    device="cpu",

    compute_type="int8"
)


def transcribe_audio(audio_data):
    """
    High accuracy transcription.
    """

    if audio_data is None:
        return ""

    if len(audio_data) == 0:
        return ""

    with tempfile.NamedTemporaryFile(

        suffix=".wav",

        delete=False

    ) as temp_audio:

        sf.write(

            temp_audio.name,

            audio_data,

            16000
        )

        segments, _ = model.transcribe(

            temp_audio.name,

            language="es",

            beam_size=5,

            vad_filter=True,

            vad_parameters=dict(
                min_silence_duration_ms=500
            )
        )

        text = " ".join(

            segment.text

            for segment in segments
        )

        return text.strip()