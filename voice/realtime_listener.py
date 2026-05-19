from voice.audio_capture import (
    record_audio
)

from voice.speech_engine import (
    transcribe_audio
)

from voice.transcript_optimizer import (
    optimize_transcript
)


def listen_realtime():
    """
    Listen realtime command.
    """

    audio_file = record_audio(
        duration=4
    )

    transcript = transcribe_audio(
        audio_file
    )

    optimized = optimize_transcript(
        transcript
    )

    return optimized