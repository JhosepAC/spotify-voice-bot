from typing import Dict, Any

"""
Spotify device management.
"""

from spotify.auth import get_spotify_client

sp = get_spotify_client()


def get_active_device() -> dict[str, Any] | None:
    """
    Get the first active Spotify device.
    """
    try:
        devices = sp.devices()

        if devices is None:
            return None

        active_devices = [
            d for d in devices.get("devices", [])
            if d.get("is_active")
        ]

        if active_devices:
            return active_devices[0]

        all_devices = devices.get("devices", [])

        if all_devices:
            return all_devices[0]

        return None

    except Exception as e:
        print(f"[Device] Error: {e}")
        return None


def validate_active_device() -> dict[str, Any]:
    """
    Get active device or raise exception.
    """
    device = get_active_device()

    if device is None:
        raise Exception(
            "No hay dispositivo Spotify activo. "
            "Abre Spotify Desktop y reproduce algo primero."
        )

    return device