from voice.listener import record_audio
from voice.whisper_engine import transcribe_audio
from voice.speaker import speak

from commands.parser import parse_command
from commands.router import route_command


def run_voice_assistant():

    try:

        speak("Listening...")

        audio_file = record_audio()

        text = transcribe_audio(audio_file)

        if not text:
            speak("I could not understand audio")
            return

        print(f"User: {text}")

        parsed_command = parse_command(text)

        response = route_command(
            parsed_command["intent"],
            parsed_command["entities"]
        )

        print(f"Assistant: {response}")

        speak(response)

    except Exception as error:

        print(error)

        speak(
            "An error occurred"
        )