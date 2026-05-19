import librosa
import noisereduce as nr
import numpy as np
import soundfile as sf


TARGET_SAMPLE_RATE = 16000

def enhance_audio(audio_path):
    """
    Clean and normalize audio.
    """

    audio, sample_rate = librosa.load(
        audio_path,
        sr=TARGET_SAMPLE_RATE
    )

    reduced_noise = nr.reduce_noise(
        y=audio,
        sr=sample_rate
    )

    normalized_audio = librosa.util.normalize(
        reduced_noise
    )

    trimmed_audio, _ = librosa.effects.trim(
        normalized_audio,
        top_db=20
    )

    output_path = audio_path.replace(
        ".wav",
        "_enhanced.wav"
    )

    sf.write(
        output_path,
        trimmed_audio,
        sample_rate
    )

    return output_path