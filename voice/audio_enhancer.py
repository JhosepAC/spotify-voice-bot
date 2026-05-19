import librosa

import noisereduce as nr

import soundfile as sf


def enhance_audio(audio_path):
    """
    Reduce microphone noise.
    """

    audio, sample_rate = librosa.load(
        audio_path,
        sr=16000
    )

    reduced_noise = nr.reduce_noise(
        y=audio,
        sr=sample_rate
    )

    enhanced_path = (
        audio_path.replace(
            ".wav",
            "_enhanced.wav"
        )
    )

    sf.write(
        enhanced_path,
        reduced_noise,
        sample_rate
    )

    return enhanced_path