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
    SEEK_FORWARD,
    SEEK_BACK,
    RESTART,
    TOGGLE,
    SKIP_N,
    SHUFFLE_ON,
    SHUFFLE_OFF,
    SHUFFLE_TOGGLE,
    REPEAT_MODE,
    QUEUE_ADD,
    QUEUE_LIST,
    MUTE,
    UNMUTE,
    VOLUME_STATUS,
    LIST_DEVICES,
    TRANSFER_DEVICE,
    UNLIKE_SONG,
    CHECK_LIKE,
    HELP,
    WHO_SINGS,
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
    handle_seek_forward,
    handle_seek_back,
    handle_restart,
    handle_toggle,
    handle_skip_n,
    handle_shuffle_on,
    handle_shuffle_off,
    handle_shuffle_toggle,
    handle_repeat_mode,
    handle_queue_add,
    handle_queue_list,
    handle_mute,
    handle_unmute,
    handle_volume_status,
    handle_unlike_song,
    handle_check_like,
    handle_list_devices,
    handle_transfer_device,
    handle_help,
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


def _handle_confirm_yes() -> str:
    """User confirmed the asked candidate: play the first pending option."""
    candidates = get_last_candidates()
    if not candidates:
        return "Perfecto, seguimos con esa."
    pick = candidates[0]
    ok = play_candidate(pick["uri"], pick.get("search_type", "track"))
    if not ok:
        return "No pude ponerla. Intenta de nuevo."
    clear_candidates()
    return f"Perfecto. Reproduciendo {pick.get('label', 'esa opción')}."


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
        return _handle_confirm_yes()

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

    if intent == SEEK_FORWARD:
        return handle_seek_forward(entities.get("seconds"))

    if intent == SEEK_BACK:
        return handle_seek_back(entities.get("seconds"))

    if intent == RESTART:
        return handle_restart()

    if intent == TOGGLE:
        return handle_toggle()

    if intent == SKIP_N:
        return handle_skip_n(entities.get("count"))

    if intent == SHUFFLE_ON:
        return handle_shuffle_on()

    if intent == SHUFFLE_OFF:
        return handle_shuffle_off()

    if intent == SHUFFLE_TOGGLE:
        return handle_shuffle_toggle()

    if intent == REPEAT_MODE:
        return handle_repeat_mode(entities.get("mode"))

    if intent == QUEUE_ADD:
        return handle_queue_add(
            entities.get("track_name"), entities.get("artist_name")
        )

    if intent == QUEUE_LIST:
        return handle_queue_list()

    if intent == MUTE:
        return handle_mute()

    if intent == UNMUTE:
        return handle_unmute()

    if intent == VOLUME_STATUS:
        return handle_volume_status()

    if intent == UNLIKE_SONG:
        return handle_unlike_song()

    if intent == CHECK_LIKE:
        return handle_check_like()

    if intent == LIST_DEVICES:
        return handle_list_devices()

    if intent == TRANSFER_DEVICE:
        return handle_transfer_device(entities.get("device_name"))

    if intent == HELP:
        return handle_help()

    if intent == WHO_SINGS:
        return handle_now_playing()

    return "No entendí ese comando."
