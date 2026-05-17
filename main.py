from voice.listener import record_audio
from voice.whisper_engine import transcribe_audio
from voice.speaker import speak


def main():
    audio_file = record_audio()

    text = transcribe_audio(audio_file)

    print(f"Usuario: {text}")

    speak(f"Has dicho: {text}")


if __name__ == "__main__":
    main()