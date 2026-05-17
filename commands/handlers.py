from spotify.player import (
    pause_playback,
    resume_playback,
    next_track,
    previous_track
)

from spotify.playback import (
    play_track
)

from spotify.library import (
    like_current_track
)


def handle_pause():
    pause_playback()

    return "Playback paused"


def handle_resume():
    resume_playback()

    return "Playback resumed"


def handle_next_track():
    next_track()

    return "Skipping track"


def handle_previous_track():
    previous_track()

    return "Previous track"


def handle_play_track(track_name):
    track = play_track(track_name)

    if not track:
        return "Track not found"

    return (
        f'Playing {track["name"]} '
        f'by {track["artist"]}'
    )


def handle_like_song():
    success = like_current_track()

    if not success:
        return "Could not like current song"

    return "Song added to liked songs"