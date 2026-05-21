"""
Voice command listener.
Captures audio from microphone with adaptive VAD,
then transcribes with Faster-Whisper.
"""

import collections
import time
import numpy as np
import sounddevice as sd

from voice.audio_config import (
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
    AUDIO_DTYPE,
    CHUNK_SIZE,
    PRE_SPEECH_BUFFER_SIZE,
    MIN_ACTIVATION_FRAMES,
    MAX_SILENCE_DURATION,
    MAX_RECORDING_SECONDS,
    MIN_SPEECH_DURATION,
    BASE_ENERGY_THRESHOLD,
    DYNAMIC_ENERGY_RATIO,
    NOISE_FLOOR_ALPHA,
    DEBUG_VAD,
)

from voice.whisper_engine import transcribe_audio
from voice.transcription_stabilizer import stabilize_transcription


class _AdaptiveVAD:
    """
    Adaptive energy-based Voice Activity Detector.
    Learns the ambient noise floor in real time.
    """

    def __init__(self):
        self.noise_floor = BASE_ENERGY_THRESHOLD

    def _energy(self, chunk: np.ndarray) -> float:
        return float(np.sqrt(np.mean(chunk ** 2)))

    def _update_floor(self, energy: float):
        self.noise_floor = (
            NOISE_FLOOR_ALPHA * self.noise_floor
            + (1 - NOISE_FLOOR_ALPHA) * energy
        )

    def threshold(self) -> float:
        return max(BASE_ENERGY_THRESHOLD, self.noise_floor * DYNAMIC_ENERGY_RATIO)

    def is_speech(self, chunk: np.ndarray) -> bool:
        energy = self._energy(chunk)
        self._update_floor(energy)
        thr = self.threshold()
        if DEBUG_VAD:
            print(f"  VAD energy={energy:.5f} thr={thr:.5f}")
        return energy > thr


_vad = _AdaptiveVAD()


def _capture_audio() -> np.ndarray:
    """
    Blocking capture: waits for speech, records until silence, returns array.
    """
    audio_frames: list[np.ndarray] = []
    pre_buffer: collections.deque = collections.deque(maxlen=PRE_SPEECH_BUFFER_SIZE)

    speech_started = False
    activation_frames = 0
    silence_frames = 0
    start_time = time.time()

    with sd.InputStream(
        samplerate=AUDIO_SAMPLE_RATE,
        channels=AUDIO_CHANNELS,
        dtype=AUDIO_DTYPE,
        blocksize=CHUNK_SIZE,
    ) as stream:

        while True:
            chunk, _ = stream.read(CHUNK_SIZE)
            chunk = chunk.flatten()

            speech = _vad.is_speech(chunk)

            if not speech_started:
                pre_buffer.append(chunk)

                if speech:
                    activation_frames += 1
                    if activation_frames >= MIN_ACTIVATION_FRAMES:
                        speech_started = True
                        audio_frames.extend(pre_buffer)
                        if DEBUG_VAD:
                            print("  VAD: speech started")
                else:
                    activation_frames = 0

            else:
                audio_frames.append(chunk)

                if speech:
                    silence_frames = 0
                else:
                    silence_frames += 1
                    silence_sec = silence_frames * (CHUNK_SIZE / AUDIO_SAMPLE_RATE)
                    if silence_sec >= MAX_SILENCE_DURATION:
                        if DEBUG_VAD:
                            print("  VAD: speech ended")
                        break

            if time.time() - start_time >= MAX_RECORDING_SECONDS:
                break

    if not audio_frames:
        return np.array([], dtype=np.float32)

    audio = np.concatenate(audio_frames)

    if len(audio) / AUDIO_SAMPLE_RATE < MIN_SPEECH_DURATION:
        return np.array([], dtype=np.float32)

    return audio


def listen_command() -> str:
    """
    Main entry: capture microphone, transcribe, stabilize.

    Returns:
        Transcribed and cleaned command string (empty string on failure).
    """
    audio = _capture_audio()

    if len(audio) == 0:
        return ""

    raw_text = transcribe_audio(audio)
    clean_text = stabilize_transcription(raw_text)

    return clean_text
