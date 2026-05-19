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

from voice.realtime_buffer import (
    RealtimeBuffer
)

from voice.stream_processor import (
    StreamProcessor
)

from voice.transcript_optimizer import (
    optimize_transcript
)


def listen_realtime():
    """
    Listen realtime speech.
    """

    recorder = StreamRecorder()

    silence_detector = (
        SilenceDetector()
    )

    audio_buffer = (
        RealtimeBuffer()
    )

    stream_processor = (
        StreamProcessor()
    )

    recorder.start()

    collector_thread = threading.Thread(
        target=recorder.collect_audio
    )

    collector_thread.start()

    processor_thread = threading.Thread(

        target=stream_processor.process_audio,

        args=(audio_buffer,)
    )

    processor_thread.start()

    print(
        "Realtime listening..."
    )

    voice_detected = False

    while True:

        audio_chunk = (
            audio_queue.get()
        )

        audio_buffer.add_chunk(
            audio_chunk
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

    stream_processor.stop()

    collector_thread.join()

    processor_thread.join()

    final_text = (
        stream_processor
        .live_transcript
        .get()
    )

    optimized = optimize_transcript(
        final_text
    )

    return optimized