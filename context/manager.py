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
