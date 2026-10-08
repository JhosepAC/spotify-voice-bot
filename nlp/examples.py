"""Paraphrase examples per intent for local fuzzy NLU.

All matching is done on normalized text (see normalizer.normalize).
Add new paraphrases here when users phrase things differently.
"""

PLAY_TRACK = [
    "pon blinding lights",
    "reproduce blinding lights",
    "toca blinding lights",
    "quiero escuchar blinding lights",
    "ponme esa cancion",
    "suena esa rola",
    "dale con esa cancion",
]

PLAY_ARTIST = [
    "pon algo de shakira",
    "pon musica de shakira",
    "reproduce algo de bad bunny",
    "quiero escuchar a karol g",
    "pon a queen",
    "toca temas de soda stereo",
]

PLAY_ALBUM = [
    "pon el album thriller",
    "reproduce el disco thriller",
    "quiero escuchar el album completo",
    "toca el disco entero",
]

PLAY_PLAYLIST = [
    "pon la playlist para estudiar",
    "reproduce mi lista de gym",
    "quiero escuchar una lista tranquila",
    "pon musica para concentrarme",
]

PAUSE = [
    "pausa",
    "dale pausa",
    "deten la musica",
    "stop",
    "silencio",
    "calla",
]

RESUME = [
    "dale play",
    "continua",
    "sigue",
    "reanuda",
    "sigue con la musica",
    "dale continua",
]

NEXT_TRACK = [
    "siguiente",
    "siguiente cancion",
    "pasa esta",
    "salta esta",
    "saltate esta",
    "la que sigue",
    "otra cancion",
]

PREVIOUS_TRACK = [
    "anterior",
    "la anterior",
    "regresa",
    "vuelve a la anterior",
    "la de antes",
]

LIKE_SONG = [
    "me gusta esta",
    "me encanta esta cancion",
    "guardala en favoritos",
    "agregala a mis me gusta",
    "dale like",
]

VOLUME_UP = [
    "sube el volumen",
    "subele",
    "mas volumen",
    "se escucha bajito subele",
    "aumenta el volumen",
]

VOLUME_DOWN = [
    "baja el volumen",
    "bajale",
    "menos volumen",
    "muy fuerte bajale",
    "disminuye el volumen",
]

SET_VOLUME = [
    "pon el volumen al 50",
    "volumen al 30",
    "ajusta el volumen a 70",
    "dejalo en 40 de volumen",
]

NOW_PLAYING = [
    "que suena",
    "que esta sonando",
    "quien canta esto",
    "como se llama esta cancion",
    "que cancion es esta",
]

CONFIRM_YES = [
    "si",
    "si esa",
    "dale si",
    "correcto",
    "exacto",
    "esa misma",
]

CONFIRM_NO = [
    "no",
    "no esa no",
    "esa no",
    "no esa, otra",
    "ninguna de esas",
    "ninguna",
    "mejor no",
]

CANCEL = [
    "cancela",
    "olvida eso",
    "dejalo",
    "nada",
    "para todo",
]

INTENT_EXAMPLES = {
    "PLAY_TRACK": PLAY_TRACK,
    "PLAY_ARTIST": PLAY_ARTIST,
    "PLAY_ALBUM": PLAY_ALBUM,
    "PLAY_PLAYLIST": PLAY_PLAYLIST,
    "PAUSE": PAUSE,
    "RESUME": RESUME,
    "NEXT_TRACK": NEXT_TRACK,
    "PREVIOUS_TRACK": PREVIOUS_TRACK,
    "LIKE_SONG": LIKE_SONG,
    "VOLUME_UP": VOLUME_UP,
    "VOLUME_DOWN": VOLUME_DOWN,
    "SET_VOLUME": SET_VOLUME,
    "NOW_PLAYING": NOW_PLAYING,
    "CONFIRM_YES": CONFIRM_YES,
    "CONFIRM_NO": CONFIRM_NO,
    "CANCEL": CANCEL,
}
