"""Update conversational memory (English identifiers, small helpers)."""

import context.state as state


def update_last_intent(intent):
    state.LAST_INTENT = intent


def update_last_track(track_name):
    state.LAST_TRACK = track_name


def update_last_artist(artist_name):
    state.LAST_ARTIST = artist_name


def update_last_album(album_name):
    state.LAST_ALBUM = album_name


def update_last_playlist(playlist_name):
    state.LAST_PLAYLIST = playlist_name


def set_last_candidates(candidates, query=None):
    state.LAST_CANDIDATES = list(candidates or [])
    state.LAST_QUERY = query


def get_last_candidates():
    return list(state.LAST_CANDIDATES or [])


def clear_candidates():
    state.LAST_CANDIDATES = []
    state.LAST_QUERY = None


def push_turn(text, intent):
    state.TURN_HISTORY.append({"text": text, "intent": intent})
    del state.TURN_HISTORY[:-10]
