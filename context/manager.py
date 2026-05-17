from context.state import CommandContext


_context = CommandContext()

def get_context():

    return _context

def update_last_intent(intent):

    _context.last_intent = intent


def update_last_track(track_name):

    _context.last_track = track_name


def update_last_artist(artist_name):

    _context.last_artist = artist_name


def update_last_album(album_name):

    _context.last_album = album_name


def update_last_playlist(playlist_name):

    _context.last_playlist = playlist_name