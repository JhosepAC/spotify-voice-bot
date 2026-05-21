"""
Faster-Whisper transcription engine.
Optimized for minimum latency on CPU with maximum accuracy.
"""

import numpy as np
from faster_whisper import WhisperModel
from voice.audio_config import (
    WHISPER_MODEL_SIZE,
    WHISPER_LANGUAGE,
    WHISPER_BEAM_SIZE,
    WHISPER_BEST_OF,
    WHISPER_TEMPERATURE,
    DEBUG_TRANSCRIPTION,
)


print("Cargando modelo Faster-Whisper...")

model = WhisperModel(
    WHISPER_MODEL_SIZE,
    device="cpu",
    compute_type="int8",
    cpu_threads=4,
    num_workers=1,
)

print(f"Modelo '{WHISPER_MODEL_SIZE}' listo.")


def transcribe_audio(audio_data: np.ndarray) -> str:
    """
    Transcribe audio to text with optimized settings.

    Args:
        audio_data: float32 numpy array at 16kHz

    Returns:
        Transcribed text string (empty on failure/silence)
    """
    if audio_data is None or len(audio_data) == 0:
        return ""

    audio_data = audio_data.astype(np.float32)
    max_val = np.max(np.abs(audio_data))
    if max_val > 1.0:
        audio_data = audio_data / max_val

    rms = np.sqrt(np.mean(audio_data ** 2))
    if rms < 0.001:
        return ""

    segments, info = model.transcribe(
        audio_data,
        language=WHISPER_LANGUAGE,
        beam_size=WHISPER_BEAM_SIZE,
        best_of=WHISPER_BEST_OF,
        temperature=WHISPER_TEMPERATURE,
        vad_filter=True,
        vad_parameters={
            "threshold": 0.4,
            "min_speech_duration_ms": 200,
            "max_speech_duration_s": 30,
            "min_silence_duration_ms": 300,
            "speech_pad_ms": 100,
        },
        word_timestamps=False,
        condition_on_previous_text=False,
        compression_ratio_threshold=2.4,
        no_speech_threshold=0.6,
        initial_prompt=(
            "Spotify. Pon, reproduce, pausa, siguiente, anterior, me gusta, "
            "volumen, artista, canción, álbum, playlist."
        ),
    )

    text = " ".join(seg.text for seg in segments).strip()

    if DEBUG_TRANSCRIPTION:
        print(f"[Whisper] '{text}' (lang={info.language}, prob={info.language_probability:.2f})")

    return text
