from voice.command_listener import (
    listen_command
)


def main():

    while True:

        print("\nSpeak...")

        text = listen_command()

        print(
            f"\nDETECTED: {text}"
        )


if __name__ == "__main__":

    main()