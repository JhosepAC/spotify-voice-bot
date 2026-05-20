import context.state as state

from spotify.player import (
    play_track,
    pause_playback,
    resume_playback,
    next_track,
    previous_track
)

from spotify.like import (
    like_current_song
)

from semantic.command_corrector import (
    correct_track_command,
    correct_artist_command
)


def handle_play_track(
    track_name
):
    """
    Play Spotify track.
    """

    corrected_track = (
        correct_track_command(
            track_name
        )
    )

    if corrected_track is None:

        return (
            "I could not find that track"
        )

    play_track(
        corrected_track
    )

    return (
        f"Playing {corrected_track}"
    )


def handle_play_artist(
    artist_name
):
    """
    Handle artist playback.
    """

    corrected_artist = (
        correct_artist_command(
            artist_name
        )
    )

    if corrected_artist is None:

        return (
            "I could not find that artist"
        )

    play_track(
        corrected_artist
    )

    return (
        f"Playing music from {corrected_artist}"
    )


def handle_play_album(
    album_name
):
    """
    Handle album playback.
    """

    if not album_name:

        return (
            "Album name missing"
        )

    play_track(
        album_name
    )

    return (
        f"Playing album {album_name}"
    )


def handle_play_playlist(
    playlist_name
):
    """
    Handle playlist playback.
    """

    if not playlist_name:

        return (
            "Playlist name missing"
        )

    play_track(
        playlist_name
    )

    return (
        f"Playing playlist {playlist_name}"
    )


def handle_repeat_last():
    """
    Repeat last contextual command.
    """

    if state.LAST_TRACK:

        return handle_play_track(
            state.LAST_TRACK
        )

    if state.LAST_ARTIST:

        return handle_play_artist(
            state.LAST_ARTIST
        )

    if state.LAST_ALBUM:

        return handle_play_album(
            state.LAST_ALBUM
        )

    if state.LAST_PLAYLIST:

        return handle_play_playlist(
            state.LAST_PLAYLIST
        )

    return (
        "There is nothing to repeat"
    )


def handle_pause():

    pause_playback()

    return "Music paused"


def handle_resume():

    resume_playback()

    return "Music resumed"


def handle_next_track():

    next_track()

    return "Skipping track"


def handle_previous_track():

    previous_track()

    return "Going back"


def handle_like_song():

    like_current_song()

    return (
        "Song added to favorites"
    )