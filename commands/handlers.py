from spotify.player import (
    pause_playback,
    resume_playback,
    next_track,
    previous_track
)

from spotify.playback import (
    play_track,
    play_artist,
    play_album,
    play_playlist
)

from spotify.library import (
    like_current_track
)

from context.manager import (
    get_context
)

from utils.response_manager import response_manager


def handle_play_artist(artist_name):

    artist = play_artist(artist_name)

    if not artist:
        return response_manager.get_response("NOT_FOUND")

    return response_manager.get_response(
        "PLAY_ARTIST", 
        artist_name=artist["name"]
    )


def handle_play_album(album_name):

    album = play_album(album_name)

    if not album:
        return response_manager.get_response("NOT_FOUND")

    return response_manager.get_response(
        "PLAY_TRACK", # Usamos una genérica o podríamos añadir PLAY_ALBUM
        track_name=album["name"],
        artist_name=""
    )


def handle_play_playlist(playlist_name):

    playlist = play_playlist(playlist_name)

    if not playlist:
        return response_manager.get_response("NOT_FOUND")

    return f'Playing playlist {playlist["name"]}' # Pendiente añadir a JSON


def handle_pause():
    pause_playback()
    return response_manager.get_response("PAUSE")


def handle_resume():
    resume_playback()
    return response_manager.get_response("RESUME")

def handle_repeat_last():

    context = get_context()

    if context.last_track:

        return handle_play_track(
            context.last_track
        )

    if context.last_artist:

        return handle_play_artist(
            context.last_artist
        )

    if context.last_album:

        return handle_play_album(
            context.last_album
        )

    if context.last_playlist:

        return handle_play_playlist(
            context.last_playlist
        )

    return "Nothing to repeat"

def handle_next_track():
    next_track()
    return response_manager.get_response("NEXT_TRACK")


def handle_previous_track():
    previous_track()
    return response_manager.get_response("PREVIOUS_TRACK")


def handle_play_track(track_name):

    track = play_track(track_name)

    if not track:
        return response_manager.get_response("NOT_FOUND")

    return response_manager.get_response(
        "PLAY_TRACK",
        track_name=track["name"],
        artist_name=track["artist"]
    )


def handle_like_song():

    success = like_current_track()

    if not success:
        return response_manager.get_response("ERROR_GENERAL")

    return response_manager.get_response("LIKE_SONG")