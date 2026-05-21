"""
Test the NLP pipeline without microphone.
Run: python tests/test_nlp.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from nlp.command_builder import build_command

TEST_COMMANDS = [
    # Reproducción
    "pon Blinding Lights de The Weeknd",
    "ponme Slow Dancing in the Dark de Joji",
    "quiero escuchar algo de Bad Bunny",
    "toca el álbum Thriller de Michael Jackson",
    "reproduce la playlist de música para estudiar",
    "pon algo relajante",
    "ponme música electrónica",
    # Control básico
    "dale pausa",
    "para la música",
    "continúa",
    "sigue",
    "siguiente canción",
    "pasa esta",
    "vuelve a la anterior",
    "regresa",
    # Like
    "me gusta esta canción",
    "agrégala a mis favoritos",
    "guárdala",
    # Volumen
    "sube el volumen",
    "baja un poco el volumen",
    "pon el volumen al 60",
    "volumen al 30 por favor",
    # Variaciones naturales difíciles
    "oye spotify pon a Shakira",
    "ey ponme la de Karol G",
    "no me gusta esta, salta",
    "quiero escuchar chill hop",
]


def main():
    print("=" * 60)
    print("TEST NLP - Spotify Voice Assistant")
    print("=" * 60)

    for cmd in TEST_COMMANDS:
        result = build_command(cmd)
        intent = result.get("intent", "None")
        entities = result.get("entities", {})
        conf = result.get("confidence", 0)

        print(f"\n📝 '{cmd}'")
        print(f"   → Intent: {intent} ({conf:.0%})")
        if entities:
            print(f"   → Entidades: {entities}")


if __name__ == "__main__":
    main()
