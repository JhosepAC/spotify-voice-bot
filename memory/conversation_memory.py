from memory.session_state import (
    SessionState
)

from memory.entity_memory import (
    EntityMemory
)


class ConversationMemory:

    def __init__(self):

        self.session = (
            SessionState()
        )

        self.entity_memory = (
            EntityMemory()
        )

    def update_context(
        self,
        intent,
        entities
    ):
        """
        Update conversation context.
        """

        self.session.last_intent = (
            intent
        )

        if "track_name" in entities:

            track = entities[
                "track_name"
            ]

            self.session.current_track = (
                track
            )

            self.entity_memory.remember(
                "track",
                track
            )

        if "artist_name" in entities:

            artist = entities[
                "artist_name"
            ]

            self.session.current_artist = (
                artist
            )

            self.entity_memory.remember(
                "artist",
                artist
            )

        if "album_name" in entities:

            album = entities[
                "album_name"
            ]

            self.session.current_album = (
                album
            )

            self.entity_memory.remember(
                "album",
                album
            )

    def get_context(self):
        """
        Get conversation state.
        """

        return self.session

    def clear(self):
        """
        Clear memory.
        """

        self.session.reset()

        self.entity_memory.clear()