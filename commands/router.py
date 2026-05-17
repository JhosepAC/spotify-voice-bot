from commands.intents import (
    PLAY_TRACK,
    PAUSE,
    RESUME,
    NEXT_TRACK,
    PREVIOUS_TRACK,
    LIKE_SONG
)

from commands.handlers import (
    handle_pause,
    handle_resume,
    handle_next_track,
    handle_previous_track,
    handle_play_track,
    handle_like_song
)


def route_command(intent, entities=None):
    """
    Route user intent to corresponding handler.

    Args:
        intent (str)
        entities (dict | None)

    Returns:
        str
    """

    entities = entities or {}

    if intent == PAUSE:
        return handle_pause()

    if intent == RESUME:
        return handle_resume()

    if intent == NEXT_TRACK:
        return handle_next_track()

    if intent == PREVIOUS_TRACK:
        return handle_previous_track()

    if intent == LIKE_SONG:
        return handle_like_song()

    if intent == PLAY_TRACK:
        track_name = entities.get("track_name")

        if not track_name:
            return "Track name missing"

        return handle_play_track(track_name)

    return "Unknown command"