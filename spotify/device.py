from spotify.auth import (
    get_spotify_client
)


sp = get_spotify_client()


def get_active_device():
    """
    Get active Spotify device.
    """

    try:

        devices_response = sp.devices()

        if not devices_response:
            return None

        devices = devices_response.get(
            "devices",
            []
        )

        if not devices:
            return None

        active_devices = [

            device

            for device in devices

            if device.get("is_active")
        ]

        if not active_devices:
            return None

        return active_devices[0]

    except Exception as error:

        print(
            f"Device Error: {error}"
        )

        return None


def validate_active_device():
    """
    Validate Spotify active device.
    """

    device = get_active_device()

    if device is None:

        raise Exception(

            "No hay un dispositivo Spotify activo. "
            "Abre Spotify Desktop y reproduce algo."

        )

    return device