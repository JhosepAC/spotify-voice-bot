from context.manager import (
    update_last_intent,
    update_last_track,
    update_last_artist,
    update_last_album,
    update_last_playlist
)

from commands.intents import (
    PLAY_ARTIST,
    PLAY_ALBUM,
    PLAY_PLAYLIST,
    REPEAT_LAST,
    PLAY_TRACK,
    PAUSE,
    RESUME,
    NEXT_TRACK,
    PREVIOUS_TRACK,
    LIKE_SONG
)

from commands.handlers import (
    handle_play_artist,
    handle_play_album,
    handle_play_playlist,
    handle_pause,
    handle_resume,
    handle_next_track,
    handle_previous_track,
    handle_repeat_last,
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

    if intent == PLAY_ARTIST:

        artist_name = entities.get(
            "artist_name"
        )

        update_last_intent(intent)

        update_last_artist(artist_name)

        return handle_play_artist(
            artist_name
        )

    if intent == PLAY_ALBUM:

        album_name = entities.get(
            "album_name"
        )

        update_last_intent(intent)

        update_last_album(album_name)

        return handle_play_album(
            album_name
        )

    if intent == PLAY_PLAYLIST:

        playlist_name = entities.get(
            "playlist_name"
        )

        update_last_intent(intent)

        update_last_playlist(
            playlist_name
        )

        return handle_play_playlist(
            playlist_name
        )

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

    if intent == REPEAT_LAST:
        return handle_repeat_last()

    if intent == PLAY_TRACK:

        track_name = entities.get("track_name")

        if not track_name:
            return "Track name missing"

        update_last_intent(intent)

        update_last_track(track_name)

    return handle_play_track(track_name)