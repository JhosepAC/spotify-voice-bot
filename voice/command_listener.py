from voice.streaming_listener import (
    StreamingListener
)

from voice.audio_preprocessor import (
    AudioPreprocessor
)

from voice.whisper_engine import (
    transcribe_audio
)


listener = StreamingListener()

preprocessor = AudioPreprocessor()


def listen_command():
    """
    Listen and transcribe command.
    """

    audio = listener.listen()

    processed_audio = (
        preprocessor.process(audio)
    )

    text = transcribe_audio(
        processed_audio
    )

    return text