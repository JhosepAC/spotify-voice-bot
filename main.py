from voice.command_listener import (
    listen_command
)


def main():

    while True:

        text = listen_command(
            duration=6
        )

        if not text:
            continue

        print(
            f"Detected: {text}"
        )


if __name__ == "__main__":
    main()