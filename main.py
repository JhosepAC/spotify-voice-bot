from spotify.search import (
    search_track,
    search_artist,
    search_album,
    search_playlist
)

tracks = search_track("Blinding Lights")

print(tracks)

artists = search_artist("Daft Punk")

print(artists)

albums = search_album("After Hours")

print(albums)

playlists = search_playlist("Lo-Fi")

print(playlists)