from voice.command_listener import (
    listen_command
)

from voice.tts_engine import (
    speak
)

from nlp.command_builder import (
    build_command
)

from commands.router import (
    route_command
)


def run_voice_assistant():
    """
    Main realtime assistant loop.
    """

    speak(
        "Spotify assistant initialized"
    )

    while True:

        try:

            text = listen_command()

            if not text:
                continue

            print(
                f"Detected: {text}"
            )

            parsed_command = build_command(
                text
            )

            intent = parsed_command.get(
                "intent"
            )

            entities = parsed_command.get(
                "entities"
            )

            if not intent:

                speak(
                    "I could not understand"
                )

                continue

            response = route_command(
                intent,
                entities
            )

            print(
                f"Assistant: {response}"
            )

            speak(response)

        except Exception as error:

            print(
                f"Pipeline Error: {error}"
            )

            speak(
                "An error occurred"
            )