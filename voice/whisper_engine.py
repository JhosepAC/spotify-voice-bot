import numpy as np

from faster_whisper import (
    WhisperModel
)

from voice.audio_config import (
    WHISPER_MODEL_SIZE,
    WHISPER_LANGUAGE,
    WHISPER_BEAM_SIZE,
    WHISPER_BEST_OF,
    WHISPER_TEMPERATURE,
    DEBUG_TRANSCRIPTION
)


print(
    "Loading Faster-Whisper model..."
)

model = WhisperModel(

    WHISPER_MODEL_SIZE,

    device="cpu",

    compute_type="int8",

    cpu_threads=8,

    num_workers=2
)


def transcribe_audio(
    audio_data: np.ndarray
):
    """
    Zero-disk realtime transcription.
    """

    if audio_data is None:

        return ""

    if len(audio_data) == 0:

        return ""

    audio_data = audio_data.astype(
        np.float32
    )

    max_value = np.max(
        np.abs(audio_data)
    )

    if max_value > 1.0:

        audio_data = (
            audio_data / max_value
        )

    segments, _ = model.transcribe(

        audio_data,

        language=WHISPER_LANGUAGE,

        beam_size=WHISPER_BEAM_SIZE,

        best_of=WHISPER_BEST_OF,

        temperature=WHISPER_TEMPERATURE,

        vad_filter=False,

        word_timestamps=False,

        condition_on_previous_text=False,

        compression_ratio_threshold=2.4,

        no_speech_threshold=0.5
    )

    text = " ".join(

        segment.text

        for segment in segments
    ).strip()

    if DEBUG_TRANSCRIPTION:

        print(
            f"TRANSCRIBED: {text}"
        )

    return text