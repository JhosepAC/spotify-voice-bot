from spotify.auth import get_spotify_client

sp = get_spotify_client()


def get_active_device():
    devices = sp.devices()

    active_devices = [
        device
        for device in devices["devices"]
        if device["is_active"]
    ]

    if not active_devices:
        return None

    return active_devices[0]


def validate_active_device():
    device = get_active_device()

    if device is None:
        raise Exception(
            "No hay un dispositivo Spotify activo. "
            "Abre Spotify Desktop y reproduce algo."
        )

    return device