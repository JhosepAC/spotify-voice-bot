from memory.conversation_memory import (
    ConversationMemory
)

from memory.reference_resolver import (
    contains_reference
)


class ContextManager:

    def __init__(self):

        self.memory = (
            ConversationMemory()
        )

    def enrich_command(
        self,
        text,
        parsed_command
    ):
        """
        Enrich command with memory.
        """

        if not contains_reference(text):
            return parsed_command

        entities = parsed_command[
            "entities"
        ]

        context = (
            self.memory.get_context()
        )

        if (
            not entities.get(
                "track_name"
            )
            and
            context.current_track
        ):

            entities[
                "track_name"
            ] = (
                context.current_track
            )

        if (
            not entities.get(
                "artist_name"
            )
            and
            context.current_artist
        ):

            entities[
                "artist_name"
            ] = (
                context.current_artist
            )

        parsed_command[
            "entities"
        ] = entities

        return parsed_command

    def update_memory(
        self,
        intent,
        entities
    ):
        """
        Update conversation memory.
        """

        self.memory.update_context(
            intent,
            entities
        )