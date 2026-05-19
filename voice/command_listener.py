from voice.streaming_listener import (
    StreamingListener
)

from voice.whisper_engine import (
    transcribe_audio
)


listener = StreamingListener()


def listen_command():
    """
    Listen and transcribe command.
    """

    audio = listener.listen()

    text = transcribe_audio(
        audio
    )

    return text