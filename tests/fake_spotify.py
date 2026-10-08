"""Offline fake for the Spotipy client used by Phase 3+ tests.

Canned search results, playback state, devices and queue plus a call
log. No network, no credentials, no hardware.
"""

SEARCH_TYPES = ("track", "artist", "album", "playlist")


class FakeSpotify:
    """Minimal Spotipy-compatible fake with inspectable calls."""

    def __init__(self):
        self.calls = []
        self.playback = {
            "is_playing": True,
            "progress_ms": 60000,
            "item": {
                "id": "t1",
                "name": "Test Song",
                "artists": [{"name": "Test Artist"}],
                "album": {"name": "Test Album"},
            },
            "device": {"volume_percent": 50},
            "shuffle_state": False,
            "repeat_state": "off",
        }
        self.device_list = [
            {"id": "d1", "name": "PC", "is_active": True},
            {"id": "d2", "name": "Celular", "is_active": False},
        ]
        self.queue_items = [
            {"uri": f"spotify:track:q{i}", "name": f"Queued {i}",
             "artists": [{"name": "Artist"}]}
            for i in range(1, 4)
        ]
        self.playlists = [
            {"id": "p1", "uri": "spotify:playlist:p1", "name": "Gym",
             "owner": {"id": "me"}},
            {"id": "p2", "uri": "spotify:playlist:p2", "name": "Chill",
             "owner": {"id": "me"}},
        ]

    # ── search ──────────────────────────────────────────────
    def search(self, q, type="track", limit=5):
        self.calls.append(("search", q, type, limit))
        items = []
        for i in range(1, limit + 1):
            item = {"uri": f"spotify:{type}:x{i}", "name": f"{q} result{i}"}
            if type in ("track", "album"):
                item["artists"] = [{"name": "Some Artist"}]
            if type == "artist":
                item["name"] = f"{q} artist{i}" if i > 1 else q
            items.append(item)
        return {f"{type}s": {"items": items}}

    # ── playback ────────────────────────────────────────────
    def start_playback(self, device_id=None, uris=None, context_uri=None):
        self.calls.append(("start_playback", device_id, uris, context_uri))
        self.playback["is_playing"] = True

    def pause_playback(self, device_id=None):
        self.calls.append(("pause_playback", device_id))
        self.playback["is_playing"] = False

    def next_track(self, device_id=None):
        self.calls.append(("next_track", device_id))

    def previous_track(self, device_id=None):
        self.calls.append(("previous_track", device_id))

    def seek_track(self, position_ms, device_id=None):
        self.calls.append(("seek_track", position_ms, device_id))
        self.playback["progress_ms"] = position_ms

    def shuffle(self, state, device_id=None):
        self.calls.append(("shuffle", state, device_id))
        self.playback["shuffle_state"] = state

    def repeat(self, state, device_id=None):
        self.calls.append(("repeat", state, device_id))
        self.playback["repeat_state"] = state

    def volume(self, volume_percent, device_id=None):
        self.calls.append(("volume", volume_percent, device_id))
        self.playback["device"]["volume_percent"] = volume_percent

    def add_to_queue(self, uri, device_id=None):
        self.calls.append(("add_to_queue", uri, device_id))

    def queue(self):
        self.calls.append(("queue",))
        return {
            "currently_playing": self.playback["item"],
            "queue": list(self.queue_items),
        }

    def current_playback(self):
        self.calls.append(("current_playback",))
        return self.playback

    def devices(self):
        self.calls.append(("devices",))
        return {"devices": list(self.device_list)}

    def transfer_playback(self, device_id, force_play=True):
        self.calls.append(("transfer_playback", device_id, force_play))

    # ── library / playlists ─────────────────────────────────
    def current_user_saved_tracks_add(self, ids):
        self.calls.append(("saved_add", list(ids)))

    def current_user_saved_tracks_delete(self, ids):
        self.calls.append(("saved_delete", list(ids)))

    def current_user_saved_tracks_contains(self, ids):
        self.calls.append(("saved_contains", list(ids)))
        return [True for _ in ids]

    def current_user_playlists(self, limit=10):
        self.calls.append(("user_playlists", limit))
        return {"items": list(self.playlists)}

    def user_playlist_create(self, user, name, public=False):
        self.calls.append(("playlist_create", user, name, public))
        new = {"id": "px", "uri": "spotify:playlist:px", "name": name}
        self.playlists.append(new)
        return new

    def playlist_add_items(self, playlist_id, items):
        self.calls.append(("playlist_add", playlist_id, list(items)))

    def current_user(self):
        return {"id": "me"}

    def called(self, name):
        return [c for c in self.calls if c[0] == name]
