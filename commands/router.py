"""Route parsed intent + entities to the correct handler."""

from typing import Optional, Dict, Any

from context.manager import (
    update_last_intent,
    update_last_track,
    update_last_artist,
    update_last_album,
    update_last_playlist,
    get_last_candidates,
    clear_candidates,
)

from commands.intents import (
    PLAY_TRACK,
    PLAY_ARTIST,
    PLAY_ALBUM,
    PLAY_PLAYLIST,
    PAUSE,
    RESUME,
    NEXT_TRACK,
    PREVIOUS_TRACK,
    LIKE_SONG,
    REPEAT_LAST,
    VOLUME_UP,
    VOLUME_DOWN,
    SET_VOLUME,
    NOW_PLAYING,
    CONFIRM_YES,
    CONFIRM_NO,
    SELECT_INDEX,
    CANCEL,
)

from commands.handlers import (
    handle_play_track,
    handle_play_artist,
    handle_play_album,
    handle_play_playlist,
    handle_pause,
    handle_resume,
    handle_next_track,
    handle_previous_track,
    handle_like_song,
    handle_now_playing,
    handle_repeat_last,
    handle_volume_up,
    handle_volume_down,
    handle_set_volume,
)

from spotify.player import play_candidate


def _handle_selection(index: int) -> str:
    """Play candidate N from the last search ("la segunda")."""
    candidates = get_last_candidates()
    if not candidates:
        return "No tengo opciones para elegir. Pide una canción primero."
    if index < 1 or index > len(candidates):
        return f"Solo tengo {len(candidates)} opciones. Di un número entre 1 y {len(candidates)}."
    pick = candidates[index - 1]
    ok = play_candidate(pick["uri"], pick.get("search_type", "track"))
    if not ok:
        return "No pude poner esa opción."
    clear_candidates()
    return f"Reproduciendo {pick.get('label', 'esa opción')}."


def _handle_confirm_no() -> str:
    """User rejected the top pick: offer the next candidate."""
    candidates = get_last_candidates()
    if len(candidates) < 2:
        return "Entendido. Dime con más detalle qué quieres escuchar."
    second = candidates[1]
    ok = play_candidate(second["uri"], second.get("search_type", "track"))
    if not ok:
        return "No pude cambiarla. Intenta de nuevo."
    clear_candidates()
    return f"Perdón por esa. Reproduciendo {second.get('label', 'la siguiente opción')}."


def route_command(intent: str, entities: Optional[Dict[str, Any]] = None) -> str:
    """
    Route user intent to corresponding handler.

    Args:
        intent (str)
        entities (dict | None)

    Returns:
        str  - response message for TTS
    """
    entities = entities or {}

    update_last_intent(intent)

    if intent == PLAY_TRACK:
        track_name = entities.get("track_name")
        artist_name = entities.get("artist_name")
        if track_name:
            update_last_track(track_name)
        if artist_name:
            update_last_artist(artist_name)
        return handle_play_track(track_name, artist_name)

    if intent == PLAY_ARTIST:
        artist_name = entities.get("artist_name")
        update_last_artist(artist_name)
        return handle_play_artist(artist_name)

    if intent == PLAY_ALBUM:
        album_name = entities.get("album_name")
        update_last_album(album_name)
        return handle_play_album(album_name)

    if intent == PLAY_PLAYLIST:
        playlist_name = entities.get("playlist_name")
        update_last_playlist(playlist_name)
        return handle_play_playlist(playlist_name)

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

    if intent == NOW_PLAYING:
        return handle_now_playing()

    if intent == SELECT_INDEX:
        return _handle_selection(int(entities.get("index", 1)))

    if intent == CONFIRM_YES:
        clear_candidates()
        return "Perfecto, seguimos con esa."

    if intent == CONFIRM_NO:
        return _handle_confirm_no()

    if intent == CANCEL:
        clear_candidates()
        return "Cancelado. ¿Qué quieres escuchar?"

    if intent == REPEAT_LAST:
        return handle_repeat_last()

    if intent == VOLUME_UP:
        return handle_volume_up()

    if intent == VOLUME_DOWN:
        return handle_volume_down()

    if intent == SET_VOLUME:
        return handle_set_volume(entities.get("volume_level"))

    return "No entendí ese comando."
