from voice.partial_transcriber import (
    transcribe_partial
)

from voice.live_transcript import (
    LiveTranscript
)

from prediction.command_predictor import (
    CommandPredictor
)

from execution.execution_manager import (
    ExecutionManager
)


class StreamProcessor:

    def __init__(self):

        self.live_transcript = (
            LiveTranscript()
        )

        self.command_predictor = (
            CommandPredictor()
        )

        self.execution_manager = (
            ExecutionManager()
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

            if not partial_text:
                continue

            self.live_transcript.update(
                partial_text
            )

            prediction = (
                self.command_predictor
                .process_partial_text(
                    partial_text
                )
            )

            print(
                f"LIVE: {partial_text}"
            )

            print(
                f"PREDICTED: "
                f"{prediction.intent}"
            )

            response = (
                self.execution_manager
                .process_prediction(
                    partial_text,
                    prediction
                )
            )

            if response:

                print(
                    f"EXECUTED: {response}"
                )

    def stop(self):
        """
        Stop processor.
        """

        self.processing = False

        self.execution_manager.reset()