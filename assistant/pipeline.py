from voice.command_listener import (
    listen_command
)

from nlp.command_builder import (
    build_command
)

from memory.memory_updater import (
    process_memory
)

from commands.router import (
    route_command
)

# AJUSTA ESTA RUTA
from voice.tts import speak


def run_voice_assistant():

    while True:

        try:

            command_text = (
                listen_command()
            )

            if not command_text:

                continue

            print(
                f"User: {command_text}"
            )

            parsed = build_command(
                command_text
            )

            parsed = process_memory(
                command_text,
                parsed
            )

            response = route_command(

                parsed["intent"],

                parsed["entities"]
            )

            print(
                f"Assistant: {response}"
            )

            speak(response)

        except Exception as error:

            print(error)

            speak(
                "An error occurred"
            )