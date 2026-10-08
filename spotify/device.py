"""Spotify device management."""

from typing import Any, Optional

from spotify.auth import get_spotify_client


def _sp():
    """Lazy client so import never needs credentials."""
    return get_spotify_client()


def get_active_device() -> Optional[dict[str, Any]]:
    """
    Get the first active Spotify device.
    """
    try:
        devices = _sp().devices()

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
