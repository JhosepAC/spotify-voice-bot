"""Conversational memory: last request plus correctable candidates."""

LAST_INTENT = None
LAST_TRACK = None
LAST_ARTIST = None
LAST_ALBUM = None
LAST_PLAYLIST = None

# Correctable candidates from the last search:
# [{"uri": str, "label": str, "search_type": str}]
LAST_CANDIDATES = []
LAST_QUERY = None

# Short turn history for debugging/telemetry: [{"text": str, "intent": str}]
TURN_HISTORY = []
