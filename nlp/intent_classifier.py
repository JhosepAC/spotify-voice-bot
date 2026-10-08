"""
Intent classifier using local Ollama LLM.
Replaces rigid keyword matching with true NLU.
Falls back to fast rule-based classifier if Ollama is unavailable.
"""

import json
import re
import requests

from config.settings import (
    OLLAMA_URL,
    OLLAMA_MODEL,
    OLLAMA_TIMEOUT,
    OLLAMA_ENABLED,
)

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
    SEEK_FORWARD,
    SEEK_BACK,
    RESTART,
    TOGGLE,
    SKIP_N,
    SHUFFLE_ON,
    SHUFFLE_OFF,
    SHUFFLE_TOGGLE,
    REPEAT_MODE,
    QUEUE_ADD,
    QUEUE_LIST,
    MUTE,
    UNMUTE,
    VOLUME_STATUS,
    LIST_DEVICES,
    TRANSFER_DEVICE,
    UNLIKE_SONG,
    CHECK_LIKE,
    HELP,
    WHO_SINGS,
    NOW_PLAYING,
    CONFIRM_YES,
    CONFIRM_NO,
    SELECT_INDEX,
    CANCEL,
    UNKNOWN,
)

from nlp.local_classifier import score_intent, HIGH_CONFIDENCE


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
- SEEK_FORWARD: adelantar segundos en la canción actual
- SEEK_BACK: retroceder segundos en la canción actual
- RESTART: reiniciar la canción desde el principio
- TOGGLE: alternar pausa/reproducción
- SKIP_N: saltar N canciones
- SHUFFLE_ON: activar modo aleatorio
- SHUFFLE_OFF: desactivar modo aleatorio
- SHUFFLE_TOGGLE: alternar modo aleatorio
- REPEAT_MODE: cambiar modo de repetición (track/context/off)
- QUEUE_ADD: agregar una canción a la cola
- QUEUE_LIST: decir qué hay en la cola
- MUTE: silenciar por completo
- UNMUTE: reactivar el sonido
- VOLUME_STATUS: decir el volumen actual
- LIST_DEVICES: listar dispositivos disponibles
- TRANSFER_DEVICE: pasar la música a otro dispositivo
- UNLIKE_SONG: quitar el me gusta actual
- CHECK_LIKE: decir si la actual está en favoritos
- HELP: explicar qué puede hacer
- WHO_SINGS: decir quién canta (igual que NOW_PLAYING)
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
  "seconds": número_entero_o_null,
  "count": número_entero_o_null,
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
    if not OLLAMA_ENABLED:
        return None
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

        # Extract JSON even if wrapped in extra text
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not match:
            return None

        return json.loads(match.group())

    except Exception as e:
        print(f"[Ollama] Error: {e}")
        return None


# ──────────────────────────────────────────────
# FALLBACK: rule-based classifier (fast)
# Used when Ollama is disabled or times out
# ──────────────────────────────────────────────

_PAUSE_RE = re.compile(
    r'\b(pau[sz]a|detener|detén|stop|silencia|calla|para la música)\b',
    re.I
)
_RESUME_RE = re.compile(
    r'\b(reanuda|continúa|continua|sigue|resume|seguir|reproduce ya|dale (play|continúa|continua|sigue))\b',
    re.I
)
_NEXT_RE = re.compile(
    r'\b(siguiente|next|skip|salta|pasa(la)?|sáltala|saltate|que sigue)\b',
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
    r'\b(volumen|vol)\b.*?(\d{1,3})\b',
    re.I
)
_DALE_PLAY_RE = re.compile(r'\bdale\s+(play|continúa|continua|sigue)\b', re.I)
_FILLER_TRACK_PREFIX_RE = re.compile(r'^(otra|esa|esta|la|el)\s+', re.I)
_SELECT_INDEX_RE = re.compile(
    r'\b(la\s+)?(primera|segunda|tercera|cuarta|quinta|[1-5])\b',
    re.I
)
_ORDINAL_MAP = {
    "primera": 1, "segunda": 2, "tercera": 3, "cuarta": 4, "quinta": 5,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
}

# Control intents resolved by precise contiguous regexes. Checked before
# fuzzy matching so stop/transport commands never lose to subset overlap
# ("para la música" must not become PLAY_PLAYLIST).
_CONTROL_INTENTS = frozenset({
    PAUSE,
    RESUME,
    NEXT_TRACK,
    PREVIOUS_TRACK,
    LIKE_SONG,
    VOLUME_UP,
    VOLUME_DOWN,
    SET_VOLUME,
    SEEK_FORWARD,
    SEEK_BACK,
    RESTART,
    TOGGLE,
    SKIP_N,
    SHUFFLE_ON,
    SHUFFLE_OFF,
    SHUFFLE_TOGGLE,
    REPEAT_MODE,
    QUEUE_LIST,
    MUTE,
    UNMUTE,
    VOLUME_STATUS,
    LIST_DEVICES,
    TRANSFER_DEVICE,
    UNLIKE_SONG,
    CHECK_LIKE,
    HELP,
    NOW_PLAYING,
})

_NUM_WORDS = {
    "una": 1, "uno": 1, "un": 1, "dos": 2, "tres": 3, "cuatro": 4,
    "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
    "quince": 15, "veinte": 20, "treinta": 30,
}


def _parse_count(text: str) -> int | None:
    """Extract a number (digits or Spanish words) from text."""
    digit = re.search(r"\b(\d{1,3})\b", text)
    if digit:
        return int(digit.group(1))
    for word, value in _NUM_WORDS.items():
        if re.search(rf"\b{word}\b", text):
            return value
    return None
_ARTIST_RE = re.compile(
    r'\b(algo de|música de|musica de|canciones de|temas de|lo de|artista|pon a)\b',
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
    r'\b(de|del|del artista|algo de|música de|musica de|canciones de|temas de)\b',
    re.I
)


def _rule_based_classify(text: str) -> dict:
    """
    Fast rule-based fallback classifier.
    Alexa-style: accept many paraphrases, avoid false positives
    when a play verb is present.
    """
    t = text.lower().strip()
    has_play_verb = bool(_PLAY_RE.search(t))

    if _DALE_PLAY_RE.search(t):
        return {"intent": RESUME, "entities": {}, "confidence": 0.9}

    if _PAUSE_RE.search(t):
        return {"intent": PAUSE, "entities": {}, "confidence": 0.9}

    skip_n = re.search(r"\b(salta|sáltate|saltate|pasa)\s+(\d{1,2}|una|uno|dos|tres|cuatro|cinco)\b", t)
    if skip_n and not has_play_verb:
        count = _parse_count(skip_n.group(0)) or 1
        return {"intent": SKIP_N, "entities": {"count": count}, "confidence": 0.9}

    if re.search(r"\b(adelanta|avanza|adelante)\b", t):
        seconds = _parse_count(t) or 30
        if re.search(r"\b(minutos?|min)\b", t):
            seconds = seconds * 60
        return {"intent": SEEK_FORWARD, "entities": {"seconds": seconds}, "confidence": 0.9}

    if re.search(r"\b(retrocede|para atr[aá]s|ve atr[aá]s)\b", t) or (
        re.search(r"\b(atr[aá]s|regresa)\b", t)
        and re.search(r"\b(segundos|seg|minutos|min)\b", t)
    ):
        seconds = _parse_count(t) or 15
        if re.search(r"\b(minutos?|min)\b", t):
            seconds = seconds * 60
        return {"intent": SEEK_BACK, "entities": {"seconds": seconds}, "confidence": 0.9}

    if re.search(
        r"\b(desde el principio|desde cero|del inicio|reinicia|vuelve a empezar|empieza de nuevo)\b",
        t,
    ):
        return {"intent": RESTART, "entities": {}, "confidence": 0.9}

    if re.search(r"\b(alterna|play pause|pausa o sigue|sigue o pausa)\b", t):
        return {"intent": TOGGLE, "entities": {}, "confidence": 0.9}

    # Transport commands win over generic "sigue" resume so that
    # "la que sigue" resolves to NEXT_TRACK, not RESUME.
    if re.search(r"\bcola\b", t) and re.search(
        r"\b(qu[eé] hay|muestra|lista|dime|ense[ñn]a|cu[aá]l sigue|que sigue)\b", t
    ):
        return {"intent": QUEUE_LIST, "entities": {}, "confidence": 0.9}

    if _NEXT_RE.search(t) and not has_play_verb:
        return {"intent": NEXT_TRACK, "entities": {}, "confidence": 0.9}

    if _PREV_RE.search(t) and not has_play_verb:
        return {"intent": PREVIOUS_TRACK, "entities": {}, "confidence": 0.9}

    if _RESUME_RE.search(t) and not has_play_verb:
        return {"intent": RESUME, "entities": {}, "confidence": 0.85}

    if re.search(
        r"\b(no me gusta|ya no me gusta|quitale el like|qu[ií]tala de favoritos|dislike)\b",
        t,
    ):
        return {"intent": UNLIKE_SONG, "entities": {}, "confidence": 0.9}

    if _LIKE_RE.search(t):
        return {"intent": LIKE_SONG, "entities": {}, "confidence": 0.9}

    if re.search(
        r"\b(est[aá] en (mis )?favoritos|ya le di like|tiene like|la tengo guardada|est[aá] guardada)\b",
        t,
    ):
        return {"intent": CHECK_LIKE, "entities": {}, "confidence": 0.85}

    if re.search(
        r"\b(qu[ií][eé]n canta|qui[eé]n es el artista|de qui[eé]n es esta|c[óo]mo se llama esta)\b",
        t,
    ):
        return {"intent": NOW_PLAYING, "entities": {}, "confidence": 0.9}

    if re.search(
        r"\b(qu[eé] suena|qu[eé] est[aá] sonando|qu[eé] canci[óo]n es esta|c[óo]mo se llama la canci[óo]n)\b",
        t,
    ):
        return {"intent": NOW_PLAYING, "entities": {}, "confidence": 0.9}

    if re.search(
        r"\b(ayuda|qu[eé] puedes hacer|qu[eé] sabes hacer|comandos|instrucciones|que puedo pedirte)\b",
        t,
    ):
        return {"intent": HELP, "entities": {}, "confidence": 0.9}

    if re.search(
        r"\b(dispositivos|en qu[eé] dispositivo|d[óo]nde est[aá] sonando|d[óo]nde suena|lista de dispositivos)\b",
        t,
    ):
        return {"intent": LIST_DEVICES, "entities": {}, "confidence": 0.9}

    transfer = re.search(
        r"\b(pasa|p[aá]salo|cambia|transfiere|ponlo|suena en)\b.{0,40}\b(celular|m[óo]vil|computadora|ordenador|pc|tablet|parlante|altavoz|bocina|tele|tv|tel[ée]fono|dispositivo|equipo|aqu[íi]|ac[áa])\b",
        t,
    )
    if transfer:
        name = re.search(r"\b(a|al|en|en el|en la)\s+(.+)$", t)
        device_name = name.group(2).strip() if name else transfer.group(0)
        return {
            "intent": TRANSFER_DEVICE,
            "entities": {"device_name": device_name},
            "confidence": 0.85,
        }

    if re.search(r"\b(mute|silenciar|enmudece|apaga el sonido|sin sonido)\b", t):
        return {"intent": MUTE, "entities": {}, "confidence": 0.9}

    if re.search(
        r"\b(unmute|activa el sonido|quita el silencio|desilencia|devuelve el sonido|vuelve el sonido|pon sonido)\b",
        t,
    ):
        return {"intent": UNMUTE, "entities": {}, "confidence": 0.9}

    if re.search(
        r"\b(en qu[eé] volumen|cu[aá]l es el volumen|a qu[eé] volumen|dime el volumen|c[óo]mo est[aá] el volumen)\b",
        t,
    ):
        return {"intent": VOLUME_STATUS, "entities": {}, "confidence": 0.9}

    if re.search(r"\b(aleatorio|shuffle|mezcla|desorden)\b", t):
        if re.search(r"\b(quita|desactiva|sin|apaga|desconecta)\b", t):
            return {"intent": SHUFFLE_OFF, "entities": {}, "confidence": 0.9}
        if re.search(r"\b(pon|activa|con|s[ií]|ponle|conecta)\b", t):
            return {"intent": SHUFFLE_ON, "entities": {}, "confidence": 0.9}
        return {"intent": SHUFFLE_TOGGLE, "entities": {}, "confidence": 0.85}

    if re.search(r"\b(repit\w*|bucle|loop|otra vez)\b", t):
        if re.search(r"\b(todo|toda|lista|[aá]lbum|cola|disco)\b", t):
            mode = "context"
        elif re.search(r"\b(no|desactiva|quita|off|para de repetir|deja de repetir)\b", t):
            mode = "off"
        else:
            mode = "track"
        return {"intent": REPEAT_MODE, "entities": {"mode": mode}, "confidence": 0.9}

    if _VOL_UP_RE.search(t):
        return {"intent": VOLUME_UP, "entities": {}, "confidence": 0.9}

    if _VOL_DOWN_RE.search(t):
        return {"intent": VOLUME_DOWN, "entities": {}, "confidence": 0.9}

    vol_set = _VOL_SET_RE.search(t)
    if vol_set:
        level = int(vol_set.group(2))
        level = max(0, min(100, level))
        return {
            "intent": SET_VOLUME,
            "entities": {"volume_level": level},
            "confidence": 0.85,
        }

    queue_add = re.search(
        r"\b(agrega|agr[ée]gala|a[ñn]ade|a[ñn]adela|mete|pon|ponme)\b.{0,50}\b(cola|fila)\b",
        t,
    )
    if queue_add:
        left = re.split(r"\b(cola|fila)\b", t, maxsplit=1)[0]
        left = re.sub(
            r"\b(agrega|agr[ée]gala|a[ñn]ade|a[ñn]adela|mete|pon|ponme|a la|en la|a|en|esta|esa|un|una|tema|canci[óo]n)\b",
            " ",
            left,
        )
        left = re.sub(r"\s+", " ", left).strip()
        queue_entities: dict = {}
        de_split = re.split(r"\bde\b", left, maxsplit=1)
        if len(de_split) == 2:
            if de_split[0].strip():
                queue_entities["track_name"] = de_split[0].strip()
            if de_split[1].strip():
                queue_entities["artist_name"] = de_split[1].strip()
        elif left:
            queue_entities["track_name"] = left
        return {"intent": QUEUE_ADD, "entities": queue_entities, "confidence": 0.8}

    # ---- Entity extraction ----
    entities = {}

    if _ALBUM_RE.search(t):
        # "play album X" -> album_name = X
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
        # Strip leading fillers from previous faulty split ("otra de X" -> "X")
        name = _FILLER_TRACK_PREFIX_RE.sub("", name).strip()

        de_split = re.split(r'\bde\b', name, maxsplit=1)
        if len(de_split) == 2:
            track = de_split[0].strip()
            artist = de_split[1].strip()
            if track:
                entities["track_name"] = track
            if artist:
                entities["artist_name"] = artist
            # "pon otra de X" / filler-only track means artist request.
            if not track and artist:
                return {"intent": PLAY_ARTIST, "entities": entities, "confidence": 0.8}
        else:
            if name:
                entities["track_name"] = name

        return {"intent": PLAY_TRACK, "entities": entities, "confidence": 0.75}

    return {"intent": UNKNOWN, "entities": {}, "confidence": 0.3}


def _detect_selection(text: str) -> dict | None:
    """Detect disambiguation picks like 'la segunda' or '2'."""
    lower = text.lower().strip()
    # A count with a skip verb is not a pick ("salta 3 canciones").
    # A bare pick ("la segunda", "pon la 3") still selects a candidate.
    if re.search(r"\b(salta|sáltate|saltate|pasa)\s+(\d{1,2}|una|uno|dos|tres|cuatro|cinco)\b", lower):
        return None
    match = _SELECT_INDEX_RE.search(lower)
    if not match:
        return None
    token = match.group(2).lower()
    index = _ORDINAL_MAP.get(token)
    if index is None:
        return None
    return {"intent": SELECT_INDEX, "entities": {"index": index}, "confidence": 0.9}


def classify_intent(text: str) -> dict:
    """
    Main intent classification (fast path first).

    Order: selection shortcut -> local fuzzy (instant) ->
    Ollama LLM (optional) -> rule-based fallback.

    No rigid shortcut: every request goes through NLU so
    paraphrases ("pon algo de X" vs "pon X") resolve correctly.

    Returns:
        {
            "intent": str,
            "entities": dict,
            "confidence": float
        }
    """
    selection = _detect_selection(text)
    if selection:
        return selection

    # Precise control commands first (contiguous regexes beat fuzzy overlap).
    early_rule = _rule_based_classify(text)
    if (
        early_rule["intent"] in _CONTROL_INTENTS
        and early_rule.get("confidence", 0.0) >= 0.85
    ):
        return early_rule

    local = score_intent(text)
    # Fast path only on decisive local matches. Close calls (low margin)
    # fall through to Ollama/rules so "la que sigue" does not lose to "sigue".
    # A play verb vetoes non-play local intents so "reproduce ... para
    # estudiar" never resolves to PAUSE via the "para" overlap.
    has_play_verb = bool(_PLAY_RE.search(text.lower()))
    play_only = (
        local["intent"] not in (PLAY_TRACK, PLAY_ARTIST, PLAY_ALBUM, PLAY_PLAYLIST)
        and has_play_verb
    )
    decisive = (
        local["intent"] != UNKNOWN
        and local["score"] >= HIGH_CONFIDENCE
        and local["confidence"] >= 0.85
        and not play_only
    )
    if decisive:
        if local["intent"] in (CONFIRM_YES, CONFIRM_NO, CANCEL, NOW_PLAYING):
            return {
                "intent": local["intent"],
                "entities": {},
                "confidence": local["confidence"],
            }
        rule_result = _rule_based_classify(text)
        if rule_result["intent"] == UNKNOWN or rule_result["intent"] == local["intent"]:
            return {
                "intent": local["intent"],
                "entities": rule_result.get("entities", {}),
                "confidence": max(local["confidence"], rule_result.get("confidence", 0.0)),
            }
        # Local intent wins for transport/mood paraphrases; keep rule entities.
        return {
            "intent": local["intent"],
            "entities": rule_result.get("entities", {}),
            "confidence": local["confidence"],
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
        if result.get("seconds") is not None:
            entities["seconds"] = int(result["seconds"])
        if result.get("count") is not None:
            entities["count"] = int(result["count"])
        if result.get("mode") in ("track", "context", "off"):
            entities["mode"] = result["mode"]

        return {
            "intent": result["intent"],
            "entities": entities,
            "confidence": float(result.get("confidence", 0.9)),
        }

    print("[NLP] Ollama unavailable or low quality, using rule-based fallback.")
    return _rule_based_classify(text)