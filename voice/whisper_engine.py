import whisper

from config.settings import (
    WHISPER_MODEL,
    WHISPER_LANGUAGE
)

print("Cargando modelo Whisper...")

model = whisper.load_model(
    WHISPER_MODEL
)


def transcribe_audio(audio_path):
    result = model.transcribe(
        audio_path,
        language=WHISPER_LANGUAGE
    )

    return result["text"].strip()