from memory.context_manager import (
    ContextManager
)


context_manager = (
    ContextManager()
)


def process_memory(
    text,
    parsed_command
):
    """
    Process conversational memory.
    """

    enriched = (
        context_manager.enrich_command(
            text,
            parsed_command
        )
    )

    context_manager.update_memory(

        enriched["intent"],

        enriched["entities"]
    )

    return enriched