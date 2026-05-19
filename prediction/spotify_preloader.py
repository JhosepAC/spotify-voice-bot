from spotify.search import (
    search_track
)


class SpotifyPreloader:

    def __init__(self):

        self.cached_results = []

    def preload_track(
        self,
        track_name
    ):
        """
        Preload Spotify search.
        """

        if not track_name:
            return

        results = search_track(
            track_name
        )

        self.cached_results = results

    def get_cached(self):
        """
        Get preloaded results.
        """

        return self.cached_results