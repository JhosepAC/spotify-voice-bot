import threading

from voice.partial_transcriber import (
    transcribe_partial
)

from voice.live_transcript import (
    LiveTranscript
)


class StreamProcessor:

    def __init__(self):

        self.live_transcript = (
            LiveTranscript()
        )

        self.processing = False

    def process_audio(
        self,
        audio_buffer
    ):
        """
        Process realtime audio.
        """

        self.processing = True

        while self.processing:

            audio_data = (
                audio_buffer.get_audio()
            )

            if audio_data is None:
                continue

            partial_text = (
                transcribe_partial(
                    audio_data
                )
            )

            if partial_text:

                self.live_transcript.update(
                    partial_text
                )

                print(
                    f"LIVE: {partial_text}"
                )

    def stop(self):
        """
        Stop processor.
        """

        self.processing = False