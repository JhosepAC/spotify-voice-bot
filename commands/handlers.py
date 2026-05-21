"""
Command handlers: map intents to Spotify actions.
"""

import context.state as state

from spotify.player import (
    play_track,
    play_artist,
    pause_playback,
    resume_playback,
    next_track,
    previous_track,
    set_volume,
    get_current_volume,
)

from spotify.like import like_current_song


def handle_play_track(track_name, artist_name=None):
    """
    Play a specific track, optionally filtered by artist.
    """
    if not track_name:
        return "No entendí el nombre de la canción."

    query = track_name
    if artist_name:
        query = f"{track_name} {artist_name}"

    success = play_track(query)

    if not success:
        return f"No encontré '{track_name}' en Spotify."

    if artist_name:
        return f"Reproduciendo {track_name} de {artist_name}."
    return f"Reproduciendo {track_name}."


def handle_play_artist(artist_name):
    """
    Play top tracks from an artist.
    """
    if not artist_name:
        return "No entendí el nombre del artista."

    success = play_artist(artist_name)

    if not success:
        return f"No encontré al artista '{artist_name}'."

    return f"Reproduciendo música de {artist_name}."


def handle_play_album(album_name):
    """
    Play an album.
    """
    if not album_name:
        return "Falta el nombre del álbum."

    success = play_track(album_name, search_type="album")

    if not success:
        return f"No encontré el álbum '{album_name}'."

    return f"Reproduciendo el álbum {album_name}."


def handle_play_playlist(playlist_name):
    """
    Play a playlist.
    """
    if not playlist_name:
        return "Falta el nombre de la playlist."

    success = play_track(playlist_name, search_type="playlist")

    if not success:
        return f"No encontré la playlist '{playlist_name}'."

    return f"Reproduciendo la playlist {playlist_name}."


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
    result = like_current_song()
    if result:
        name = result.get("track_name", "esta canción")
        return f"¡{name} agregada a tus favoritos!"
    return "No hay ninguna canción en reproducción."


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
