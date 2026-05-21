from voice.command_listener import (
    listen_command
)


def main():

    while True:

        print("\nSpeak...")

        text = listen_command()

        if not text:

            print(
                "\nREJECTED TRANSCRIPTION"
            )

            continue

        print(
            f"\nDETECTED: {text}"
        )


if __name__ == "__main__":

    main()