from voice.audio_capture import (
    record_audio
)

from voice.speech_engine import (
    transcribe_audio
)

from voice.transcript_optimizer import (
    optimize_transcript
)

from utils.file_manager import safe_remove
import os



def listen_command(duration=6):
    """
    Listen and process command.
    """

    audio_file = record_audio(
        duration=duration
    )

    try:
        transcript = transcribe_audio(
            audio_file
        )

        optimized_text = optimize_transcript(
            transcript
        )
        
        return optimized_text
    
    finally:
        # Limpieza: eliminamos el original y el mejorado si existe
        safe_remove(audio_file)
        enhanced_path = audio_file.replace(".wav", "_enhanced.wav")
        safe_remove(enhanced_path)