from voice.streaming_listener import (
    StreamingListener
)

from voice.incremental_transcriber import (
    IncrementalTranscriber
)


listener = StreamingListener()

transcriber = (
    IncrementalTranscriber()
)


def listen_command():
    """
    Incremental realtime listening.
    """

    print(
        "Listening realtime..."
    )

    audio = listener.listen()

    if len(audio) == 0:

        return ""

    transcriber.add_audio(
        audio
    )

    partial = (
        transcriber.get_partial_transcription()
    )

    if partial:

        print(
            f"PARTIAL: {partial}"
        )

    final_text = (
        transcriber.finalize()
    )

    return final_text