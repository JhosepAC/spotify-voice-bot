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

SEEK_FORWARD = [
    "adelanta 30 segundos",
    "avanza un poco",
    "adelanta la cancion",
    "salta hacia adelante",
]

SEEK_BACK = [
    "retrocede 15 segundos",
    "ve para atras",
    "regresa un poco la cancion",
    "devuelvete unos segundos",
]

RESTART = [
    "desde el principio",
    "reinicia la cancion",
    "del inicio otra vez",
    "vuelve a empezar",
]

TOGGLE = [
    "alterna",
    "pausa o sigue",
    "play pause",
]

SKIP_N = [
    "salta 3 canciones",
    "pasa 2 temas",
    "saltate 5",
]

SHUFFLE_ON = [
    "pon en aleatorio",
    "activa el aleatorio",
    "mezcla las canciones",
    "con shuffle",
]

SHUFFLE_OFF = [
    "quita el aleatorio",
    "desactiva la mezcla",
    "sin aleatorio",
]

SHUFFLE_TOGGLE = [
    "aleatorio",
    "cambia el aleatorio",
    "shuffle",
]

REPEAT_MODE = [
    "repite esta cancion",
    "repite todo",
    "pon en bucle",
    "no repitas",
    "repite otra vez",
]

QUEUE_ADD = [
    "agrega esta a la cola",
    "pon esa cancion en la cola",
    "mete la siguiente a la cola",
    "añade un tema a la cola",
]

QUEUE_LIST = [
    "que hay en la cola",
    "muestra la cola",
    "cual sigue en la cola",
    "dime la cola",
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
    "SEEK_FORWARD": SEEK_FORWARD,
    "SEEK_BACK": SEEK_BACK,
    "RESTART": RESTART,
    "TOGGLE": TOGGLE,
    "SKIP_N": SKIP_N,
    "SHUFFLE_ON": SHUFFLE_ON,
    "SHUFFLE_OFF": SHUFFLE_OFF,
    "SHUFFLE_TOGGLE": SHUFFLE_TOGGLE,
    "REPEAT_MODE": REPEAT_MODE,
    "QUEUE_ADD": QUEUE_ADD,
    "QUEUE_LIST": QUEUE_LIST,
}
