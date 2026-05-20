import context.state as state


def update_last_intent(
    intent
):
    """
    Update last intent.
    """

    state.LAST_INTENT = intent


def update_last_track(
    track_name
):
    """
    Update last track.
    """

    state.LAST_TRACK = track_name


def update_last_artist(
    artist_name
):
    """
    Update last artist.
    """

    state.LAST_ARTIST = artist_name


def update_last_album(
    album_name
):
    """
    Update last album.
    """

    state.LAST_ALBUM = album_name


def update_last_playlist(
    playlist_name
):
    """
    Update last playlist.
    """

    state.LAST_PLAYLIST = playlist_name