from voice.audio_capture import (
    record_audio
)

from voice.speech_engine import (
    transcribe_audio
)

from voice.transcript_optimizer import (
    optimize_transcript
)



def listen_command(duration=6):
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

    return optimized_text