import sounddevice as sd
from scipy.io.wavfile import write


def record_audio(
    filename="temp/audio.wav",
    duration=5,
    sample_rate=44100
):
    print("Grabando audio...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write(filename, sample_rate, recording)

    print("Grabación finalizada")

    return filename