"""
Intent classifier using local Ollama LLM.
Replaces rigid keyword matching with true NLU.
Falls back to fast rule-based classifier if Ollama is unavailable.
"""

import json
import re
import requests

from commands.intents import (
    PLAY_TRACK,
    PLAY_ARTIST,
    PLAY_ALBUM,
    PLAY_PLAYLIST,
    PAUSE,
    RESUME,
    NEXT_TRACK,
    PREVIOUS_TRACK,
    LIKE_SONG,
    REPEAT_LAST,
    VOLUME_UP,
    VOLUME_DOWN,
    SET_VOLUME,
    UNKNOWN,
)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "phi3"          # phi3 = muy liviano (~2GB), rápido, excelente NLU
OLLAMA_TIMEOUT = 4             # segundos máximo de espera


SYSTEM_PROMPT = """Eres el clasificador de intenciones de un asistente de voz para Spotify.
Tu única tarea es analizar el comando del usuario y responder ÚNICAMENTE con un JSON válido.

Intenciones disponibles:
- PLAY_TRACK: reproducir una canción específica
- PLAY_ARTIST: reproducir música de un artista
- PLAY_ALBUM: reproducir un álbum
- PLAY_PLAYLIST: reproducir una playlist
- PAUSE: pausar la música
- RESUME: reanudar/continuar la música
- NEXT_TRACK: siguiente canción
- PREVIOUS_TRACK: canción anterior
- LIKE_SONG: dar me gusta / guardar en favoritos la canción actual
- VOLUME_UP: subir el volumen
- VOLUME_DOWN: bajar el volumen
- SET_VOLUME: establecer volumen a un valor concreto
- REPEAT_LAST: repetir lo último
- UNKNOWN: no se entiende la intención

Responde SOLO con este JSON (sin texto adicional, sin markdown):
{
  "intent": "INTENT_NAME",
  "track_name": "nombre de la canción o null",
  "artist_name": "nombre del artista o null",
  "album_name": "nombre del álbum o null",
  "playlist_name": "nombre de la playlist o null",
  "volume_level": número_entero_o_null,
  "confidence": 0.0_a_1.0
}

Ejemplos:
- "pon Blinding Lights de The Weeknd" → PLAY_TRACK, track_name="Blinding Lights", artist_name="The Weeknd"
- "pon algo de Shakira" → PLAY_ARTIST, artist_name="Shakira"
- "quiero escuchar el álbum Thriller" → PLAY_ALBUM, album_name="Thriller"
- "dale pausa" → PAUSE
- "sube el volumen" → VOLUME_UP
- "pon el volumen al 50" → SET_VOLUME, volume_level=50
- "me gusta esta" → LIKE_SONG
- "pasa la" → NEXT_TRACK
- "reproduce algo relajante" → PLAY_PLAYLIST, playlist_name="relajante"
"""


def _call_ollama(text: str) -> dict | None:
    """
    Call local Ollama for intent classification.
    Returns parsed dict or None on failure.
    """
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": f"{SYSTEM_PROMPT}\n\nComando del usuario: \"{text}\"",
            "stream": False,
            "options": {
                "temperature": 0.0,
                "num_predict": 120,
                "top_k": 1,
            },
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=OLLAMA_TIMEOUT
        )

        if response.status_code != 200:
            return None

        raw = response.json().get("response", "").strip()

        print(f"\n[OLLAMA RAW]\n{raw}\n")

        # Extraer JSON aunque venga con texto extra
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not match:
            return None

        return json.loads(match.group())

    except Exception as e:
        print(f"[Ollama] Error: {e}")
        return None


# ──────────────────────────────────────────────
# FALLBACK: clasificador por reglas (rápido)
# Se usa cuando Ollama no responde a tiempo
# ──────────────────────────────────────────────
_DIRECT_PLAY_RE = re.compile(
    r'^(pon|reproduce|toca|play|ponme)\s+(.+)$',
    re.I
)

_PAUSE_RE = re.compile(
    r'\b(pau[sz]a|detener|detén|stop|silencia|calla|para la música)\b',
    re.I
)
_RESUME_RE = re.compile(
    r'\b(reanuda|continúa|sigue|resume|play|reproduce ya|dale|seguir)\b',
    re.I
)
_NEXT_RE = re.compile(
    r'\b(siguiente|otra|next|skip|salta|pasa(la)?|cambia)\b',
    re.I
)
_PREV_RE = re.compile(
    r'\b(anterior|previa|regresa|atrás|vuelve|back|repite la anterior)\b',
    re.I
)
_LIKE_RE = re.compile(
    r'\b(me gusta|favorita|like|guarda(la)?|agrégala|añade a (mis )?favoritos)\b',
    re.I
)
_VOL_UP_RE = re.compile(
    r'\b(sube|aumenta|más volumen|sube el volumen|louder)\b',
    re.I
)
_VOL_DOWN_RE = re.compile(
    r'\b(baja|disminuye|menos volumen|baja el volumen|quieter)\b',
    re.I
)
_VOL_SET_RE = re.compile(
    r'\b(pon|pone|sube|baja|coloca|ajusta).{0,20}(volumen|vol).{0,10}(\d{1,3})\b',
    re.I
)
_ARTIST_RE = re.compile(
    r'\b(algo de|música de|canciones de|temas de|lo de|artista|pon a)\b',
    re.I
)
_ALBUM_RE = re.compile(
    r'\b(álbum|album|disco)\b',
    re.I
)
_PLAYLIST_RE = re.compile(
    r'\b(playlist|lista|lista de reproducción|lista de canciones)\b',
    re.I
)
_PLAY_RE = re.compile(
    r'\b(pon|reproduce|toca|quiero escuchar|quiero oír|escuchar|play|ponme)\b',
    re.I
)
_TRACK_SPLIT_RE = re.compile(
    r'\b(pon|reproduce|toca|quiero escuchar|quiero oír|escuchar|play|ponme|oye spotify|ey spotify|eh spotify)\b',
    re.I
)
_ARTIST_SPLIT_RE = re.compile(
    r'\b(de|del|del artista|algo de|música de|canciones de|temas de)\b',
    re.I
)


def _rule_based_classify(text: str) -> dict:
    """
    Fast rule-based fallback classifier.
    """
    t = text.lower().strip()

    if _PAUSE_RE.search(t):
        return {"intent": PAUSE, "entities": {}, "confidence": 0.9}

    if _RESUME_RE.search(t) and not _PLAY_RE.search(t):
        return {"intent": RESUME, "entities": {}, "confidence": 0.85}

    if _NEXT_RE.search(t):
        return {"intent": NEXT_TRACK, "entities": {}, "confidence": 0.9}

    if _PREV_RE.search(t):
        return {"intent": PREVIOUS_TRACK, "entities": {}, "confidence": 0.9}

    if _LIKE_RE.search(t):
        return {"intent": LIKE_SONG, "entities": {}, "confidence": 0.9}

    if _VOL_UP_RE.search(t):
        return {"intent": VOLUME_UP, "entities": {}, "confidence": 0.9}

    if _VOL_DOWN_RE.search(t):
        return {"intent": VOLUME_DOWN, "entities": {}, "confidence": 0.9}

    vol_set = _VOL_SET_RE.search(t)
    if vol_set:
        level = int(vol_set.group(3))
        return {
            "intent": SET_VOLUME,
            "entities": {"volume_level": level},
            "confidence": 0.85,
        }

    # ---- Extracción de nombre ----
    entities = {}

    if _ALBUM_RE.search(t):
        # "reproduce el álbum X" → album_name = X
        album = re.split(r'\b(álbum|album|disco)\b', t, maxsplit=1, flags=re.I)
        name = album[-1].strip().lstrip('de').strip() if len(album) > 1 else ""
        if name:
            entities["album_name"] = name
        return {"intent": PLAY_ALBUM, "entities": entities, "confidence": 0.8}

    if _PLAYLIST_RE.search(t):
        pl = re.split(r'\b(playlist|lista)\b', t, maxsplit=1, flags=re.I)
        name = pl[-1].strip().lstrip('de').strip() if len(pl) > 1 else ""
        if name:
            entities["playlist_name"] = name
        return {"intent": PLAY_PLAYLIST, "entities": entities, "confidence": 0.8}

    if _ARTIST_RE.search(t):
        parts = _ARTIST_SPLIT_RE.split(t)
        name = parts[-1].strip() if parts else ""
        if name:
            entities["artist_name"] = name
        return {"intent": PLAY_ARTIST, "entities": entities, "confidence": 0.8}

    if _PLAY_RE.search(t):
        parts = _TRACK_SPLIT_RE.split(t)
        name = parts[-1].strip() if parts else t

        de_split = re.split(r'\bde\b', name, maxsplit=1)
        if len(de_split) == 2:
            track = de_split[0].strip()
            artist = de_split[1].strip()
            if track:
                entities["track_name"] = track
            if artist:
                entities["artist_name"] = artist
        else:
            if name:
                entities["track_name"] = name

        return {"intent": PLAY_TRACK, "entities": entities, "confidence": 0.75}

    return {"intent": UNKNOWN, "entities": {}, "confidence": 0.3}


def classify_intent(text: str) -> dict:
    """
    Main intent classification.
    Tries Ollama first (LLM-based NLU), falls back to rules.

    Returns:
        {
            "intent": str,
            "entities": dict,
            "confidence": float
        }
    """

    direct = _DIRECT_PLAY_RE.match(text.strip())

    if direct:
        possible_track = direct.group(2).strip()

        return {
            "intent": PLAY_TRACK,
            "entities": {
            "track_name": possible_track
            },
            "confidence": 0.95,
        }

    result = _call_ollama(text)

    if result and result.get("intent"):
        entities = {}

        if result.get("track_name"):
            entities["track_name"] = result["track_name"]
        if result.get("artist_name"):
            entities["artist_name"] = result["artist_name"]
        if result.get("album_name"):
            entities["album_name"] = result["album_name"]
        if result.get("playlist_name"):
            entities["playlist_name"] = result["playlist_name"]
        if result.get("volume_level") is not None:
            entities["volume_level"] = int(result["volume_level"])

        return {
            "intent": result["intent"],
            "entities": entities,
            "confidence": float(result.get("confidence", 0.9)),
        }

    print("[NLP] Ollama falló realmente.")
    return _rule_based_classify(text)