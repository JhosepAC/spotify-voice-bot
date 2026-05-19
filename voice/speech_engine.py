from typing import cast
import whisper

from voice.audio_enhancer import enhance_audio

print("Loading Whisper model...")

model = whisper.load_model("small")


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe audio using Whisper.
    """

    enhanced_audio = enhance_audio(audio_path)

    result = model.transcribe(
        enhanced_audio,
        language="es",
        task="transcribe",
        fp16=False,
        temperature=0,
        beam_size=5,
        best_of=5
    )

    text = cast(str, result["text"])

    text = text.strip()

    return text