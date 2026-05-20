from voice.command_listener import (
    listen_command
)

from voice.tts import (
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

    print(
        "\nSpotify Voice Assistant Ready\n"
    )

    while True:

        try:

            print(
                "\nListening..."
            )

            command_text = (
                listen_command()
            )

            if not command_text:

                continue

            print(
                f"\nUSER: {command_text}"
            )

            parsed = build_command(
                command_text
            )

            print(
                f"\nPARSED: {parsed}"
            )

            intent = parsed.get(
                "intent"
            )

            entities = parsed.get(
                "entities",
                {}
            )

            if intent is None:

                response = (
                    "I could not understand the command"
                )

                print(
                    f"\nASSISTANT: {response}"
                )

                speak(response)

                continue

            response = route_command(

                intent,

                entities
            )

            print(
                f"\nASSISTANT: {response}"
            )

            speak(response)

        except Exception as error:

            print(
                f"\nERROR: {error}"
            )

            speak(
                "An error occurred"
            )