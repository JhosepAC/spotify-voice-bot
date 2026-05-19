import threading

from voice.stream_recorder import (
    StreamRecorder,
    audio_queue
)

from voice.audio_chunker import (
    chunk_to_bytes
)

from voice.realtime_vad import (
    detect_voice
)

from voice.silence_detector import (
    SilenceDetector
)

from voice.speech_engine import (
    transcribe_audio
)

from voice.transcript_optimizer import (
    optimize_transcript
)


def listen_realtime():
    """
    Listen realtime speech dynamically.
    """

    recorder = StreamRecorder()

    silence_detector = (
        SilenceDetector()
    )

    recorder.start()

    collector_thread = threading.Thread(
        target=recorder.collect_audio
    )

    collector_thread.start()

    print(
        "Listening realtime..."
    )

    voice_detected = False

    while True:

        audio_chunk = (
            audio_queue.get()
        )

        audio_bytes = (
            chunk_to_bytes(
                audio_chunk
            )
        )

        has_voice = detect_voice(
            audio_bytes
        )

        if has_voice:

            voice_detected = True

            silence_detector.update()

        if (
            voice_detected
            and
            silence_detector.silence_exceeded()
        ):

            break

    recorder.stop()

    collector_thread.join()

    audio_path = (
        recorder.save_audio()
    )

    transcript = transcribe_audio(
        audio_path
    )

    optimized = optimize_transcript(
        transcript
    )

    return optimized