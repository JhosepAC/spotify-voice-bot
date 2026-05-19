from voice.audio_capture import (
    record_audio
)

from voice.speech_engine import (
    transcribe_audio
)

from voice.language_optimizer import (
    optimize_transcript
)

from voice.transcript_validator import (
    validate_transcript
)

def listen_command(duration=5):
    """
    Listen and process command.
    """

    audio_file = record_audio(
        duration=duration
    )

    transcript = transcribe_audio(
        audio_file
    )

    optimized_text = optimize_transcript(
        transcript
    )

    is_valid = validate_transcript(
        optimized_text
    )

    if not is_valid:
        return None

    return optimized_text