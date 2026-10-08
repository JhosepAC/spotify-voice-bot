"""Command handlers: map intents to Spotify actions."""

import context.state as state

from spotify.player import (
    resolve_and_play,
    resolve_artist,
    pause_playback,
    resume_playback,
    next_track,
    previous_track,
    set_volume,
    get_current_volume,
    get_current_track,
)

from spotify.like import like_current_song


def handle_play_track(track_name, artist_name=None):
    """
    Play a specific track, optionally filtered by artist.
    Speaks back the API-verified title, not the raw transcript.
    """
    if not track_name and not artist_name:
        return "No entendí el nombre de la canción."

    query = track_name or ""
    if artist_name:
        query = f"{query} {artist_name}".strip()

    result = resolve_and_play(query, search_type="track")
    if not result.get("success"):
        spoken = query or "esa canción"
        return f"No encontré '{spoken}' en Spotify."

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
