import queue

import tempfile

import threading

import numpy as np

import sounddevice as sd

import soundfile as sf


SAMPLE_RATE = 16000

CHANNELS = 1

BLOCKSIZE = 480


audio_queue = queue.Queue()


def audio_callback(
    indata,
    frames,
    time,
    status
):
    """
    Stream microphone callback.
    """

    if status:
        print(status)

    audio_queue.put(
        indata.copy()
    )


class StreamRecorder:

    def __init__(self):

        self.recording = False

        self.frames = []

    def start(self):
        """
        Start stream recording.
        """

        self.recording = True

        self.frames = []

        self.stream = sd.InputStream(

            samplerate=SAMPLE_RATE,

            channels=CHANNELS,

            blocksize=BLOCKSIZE,

            callback=audio_callback
        )

        self.stream.start()

    def stop(self):
        """
        Stop stream recording.
        """

        self.recording = False

        self.stream.stop()

        self.stream.close()

    def collect_audio(self):
        """
        Collect realtime chunks.
        """

        while self.recording:

            audio_chunk = (
                audio_queue.get()
            )

            self.frames.append(
                audio_chunk
            )

    def save_audio(self):
        """
        Save stream audio.
        """

        audio_data = np.concatenate(
            self.frames,
            axis=0
        )

        temp_file = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        sf.write(
            temp_file.name,
            audio_data,
            SAMPLE_RATE
        )

        return temp_file.name