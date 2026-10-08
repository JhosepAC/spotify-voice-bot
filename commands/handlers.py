"""Command handlers: map intents to Spotify actions."""

import context.state as state
from config.settings import LOW_CONFIRM_THRESHOLD
from context.manager import set_last_candidates

from spotify.player import (
    preview_candidates,
    resolve_and_play,
    resolve_artist,
    pause_playback,
    resume_playback,
    next_track,
    previous_track,
    seek_forward,
    seek_back,
    restart_track,
    toggle_playback,
    skip_n,
    set_shuffle,
    toggle_shuffle,
    set_repeat_mode,
    queue_track,
    get_queue_labels,
    mute,
    unmute,
    list_device_names,
    transfer_to_device,
    set_volume,
    get_current_volume,
    get_current_track,
)

from spotify.like import like_current_song, unlike_current_song, is_current_song_liked


def _maybe_confirm(query: str, search_type: str):
    """
    Preview search results before playing.

    Returns (action, payload) where action is "play", "ask" or "miss".
    Low fuzzy scores ask the user instead of playing the wrong item.
    """
    preview = preview_candidates(query, search_type)
    label = preview.get("label")
    score = preview.get("score", 0.0)
    if not label:
        return "miss", preview
    if score < LOW_CONFIRM_THRESHOLD:
        set_last_candidates(preview.get("candidates", []), query=query)
        return "ask", preview
    return "play", preview


def handle_play_track(track_name, artist_name=None):
    """
    Play a specific track, optionally filtered by artist.
    Speaks back the API-verified title, not the raw transcript.
    Asks for confirmation on low fuzzy scores.
    """
    if not track_name and not artist_name:
        return "No entendí el nombre de la canción."

    query = track_name or ""
    if artist_name:
        query = f"{query} {artist_name}".strip()

    action, preview = _maybe_confirm(query, "track")
    if action == "miss":
        spoken = query or "esa canción"
        return f"No encontré '{spoken}' en Spotify."
    if action == "ask":
        return (
            f"No estoy segura. ¿Quisiste decir {preview.get('label')}? "
            "Di sí, o la segunda."
        )

    result = resolve_and_play(query, search_type="track")
    if not result.get("success"):
        spoken = query or "esa canción"
        return f"No encontré '{spoken}' en Spotify."

    set_last_candidates(
        [{**c, "search_type": "track"} for c in result.get("candidates", [])],
        query=query,
    )
    return f"Reproduciendo {result.get('label', query)}."


def handle_play_artist(artist_name):
    """
    Play top tracks from an artist.
    """
    if not artist_name:
        return "No entendí el nombre del artista."

    result = resolve_artist(artist_name)
    if not result.get("success"):
        return f"No encontré al artista '{artist_name}'."

    return f"Reproduciendo música de {result.get('label', artist_name)}."


def handle_play_album(album_name):
    """
    Play an album.
    """
    if not album_name:
        return "Falta el nombre del álbum."

    result = resolve_and_play(album_name, search_type="album")
    if not result.get("success"):
        return f"No encontré el álbum '{album_name}'."

    return f"Reproduciendo el álbum {result.get('label', album_name)}."


def handle_play_playlist(playlist_name):
    """
    Play a playlist.
    """
    if not playlist_name:
        return "Falta el nombre de la playlist."

    result = resolve_and_play(playlist_name, search_type="playlist")
    if not result.get("success"):
        return f"No encontré la playlist '{playlist_name}'."

    return f"Reproduciendo la playlist {result.get('label', playlist_name)}."


def handle_pause():
    pause_playback()
    return "Música pausada."


def handle_resume():
    resume_playback()
    return "Continuamos con la música."


def handle_next_track():
    next_track()
    return "Siguiente canción."


def handle_previous_track():
    previous_track()
    return "Volviendo a la anterior."


def handle_like_song():
    """Like the current track, with graceful fallback when idle."""
    try:
        result = like_current_song()
    except Exception:
        return "No hay ninguna canción en reproducción."
    if result:
        name = result.get("track_name", "esta canción")
        return f"¡{name} agregada a tus favoritos!"
    return "No hay ninguna canción en reproducción."


def handle_now_playing():
    """Tell the user what is currently playing (verified by API)."""
    track = get_current_track()
    if not track:
        return "No hay nada sonando ahora mismo."
    return f"Suena {track.get('name')} de {track.get('artist')}."


def handle_volume_up():
    current = get_current_volume()
    new_vol = min(100, current + 15)
    set_volume(new_vol)
    return f"Volumen subido a {new_vol}."


def handle_volume_down():
    current = get_current_volume()
    new_vol = max(0, current - 15)
    set_volume(new_vol)
    return f"Volumen bajado a {new_vol}."


def handle_set_volume(level):
    if level is None:
        return "No entendí el nivel de volumen."
    level = max(0, min(100, int(level)))
    set_volume(level)
    return f"Volumen ajustado a {level}."


def handle_seek_forward(seconds=None):
    seconds = int(seconds) if seconds else 30
    pos = seek_forward(seconds)
    if pos < 0:
        return "No pude adelantar. ¿Hay algo sonando?"
    return f"Adelantados {seconds} segundos."


def handle_seek_back(seconds=None):
    seconds = int(seconds) if seconds else 15
    pos = seek_back(seconds)
    if pos < 0:
        return "No pude retroceder. ¿Hay algo sonando?"
    return f"Retrocedidos {seconds} segundos."


def handle_restart():
    if restart_track():
        return "De nuevo desde el principio."
    return "No pude reiniciar la canción."


def handle_toggle():
    result = toggle_playback()
    if result == "paused":
        return "Pausado."
    if result == "playing":
        return "Sigamos con la música."
    return "No hay nada sonando para alternar."


def handle_skip_n(count=None):
    count = max(1, min(20, int(count) if count else 1))
    done = skip_n(count)
    if done <= 0:
        return "No pude saltar canciones."
    if done == 1:
        return "Siguiente canción."
    return f"Saltadas {done} canciones."


def handle_shuffle_on():
    if not set_shuffle(True):
        return "No pude activar el aleatorio."
    return "Aleatorio activado."


def handle_shuffle_off():
    if not set_shuffle(False):
        return "No pude quitar el aleatorio."
    return "Aleatorio desactivado."


def handle_shuffle_toggle():
    result = toggle_shuffle()
    if result is None:
        return "No pude cambiar el aleatorio."
    return "Aleatorio activado." if result else "Aleatorio desactivado."


def handle_repeat_mode(mode=None):
    mode = mode if mode in ("track", "context", "off") else "track"
    if not set_repeat_mode(mode):
        return "No pude cambiar la repetición."
    if mode == "track":
        return "Repitiendo esta canción."
    if mode == "context":
        return "Repitiendo todo."
    return "Repetición desactivada."


def handle_queue_add(track_name=None, artist_name=None):
    query = (track_name or "").strip()
    if artist_name:
        query = f"{query} {artist_name}".strip()
    if not query:
        return "No entendí qué agregar a la cola."
    result = queue_track(query)
    if not result.get("success"):
        return f"No encontré '{query}' en Spotify."
    return f"{result.get('label', query)} agregada a la cola."


def handle_queue_list():
    labels = get_queue_labels(3)
    if not labels:
        return "La cola está vacía."
    if len(labels) == 1:
        return f"En la cola sigue {labels[0]}."
    return "En la cola siguen " + ", ".join(labels[:-1]) + f" y {labels[-1]}."


def handle_mute():
    previous = mute()
    if previous is None:
        return "No pude silenciar."
    return "Silenciado."


def handle_unmute():
    level = unmute()
    if level < 0:
        return "No pude reactivar el sonido."
    return f"Sonido de vuelta al {level}."


def handle_volume_status():
    level = get_current_volume()
    return f"El volumen está al {level}."


def handle_unlike_song():
    try:
        result = unlike_current_song()
    except Exception:
        return "No hay ninguna canción en reproducción."
    if result:
        name = result.get("track_name", "esa canción")
        return f"{name} quitada de tus favoritos."
    return "No hay ninguna canción en reproducción."


def handle_check_like():
    try:
        if is_current_song_liked():
            return "Esta ya está en tus favoritos."
        return "Esta aún no está en tus favoritos."
    except Exception:
        return "No hay ninguna canción en reproducción."


def handle_list_devices():
    devices = list_device_names()
    if not devices:
        return "No veo ningún dispositivo. Abre Spotify en alguno primero."
    names = [d["name"] for d in devices]
    active = next((d["name"] for d in devices if d.get("active")), None)
    listing = ", ".join(names)
    if active:
        return f"Dispositivos: {listing}. Está sonando en {active}."
    return f"Dispositivos: {listing}."


def handle_transfer_device(device_name=None):
    if not device_name:
        return "¿A qué dispositivo lo paso?"
    result = transfer_to_device(device_name)
    if not result.get("success"):
        return f"No encontré el dispositivo '{device_name}'."
    return f"Pasando la música a {result.get('label', device_name)}."


def handle_help():
    return (
        "Puedo poner canciones, artistas, álbumes y playlists, pausar, seguir, "
        "adelantar, repetir, aleatorio, cola, volumen, dispositivos, favoritos "
        "y decirte qué suena. Por ejemplo: pon algo de Shakira, adelanta 30 segundos, "
        "agrega esta a la cola, o pásalo al celular."
    )


def handle_repeat_last():
    """
    Repeat last contextual command.
    """
    if state.LAST_TRACK:
        return handle_play_track(state.LAST_TRACK, state.LAST_ARTIST)

    if state.LAST_ARTIST:
        return handle_play_artist(state.LAST_ARTIST)

    if state.LAST_ALBUM:
        return handle_play_album(state.LAST_ALBUM)

    if state.LAST_PLAYLIST:
        return handle_play_playlist(state.LAST_PLAYLIST)

    return "No hay nada que repetir."
