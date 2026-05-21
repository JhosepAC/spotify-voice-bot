"""
Main assistant pipeline.
Orchestrates: wake word → listen → NLP → route → speak
"""

import random
import json
import os

from voice.command_listener import listen_command
from voice.tts import speak
from nlp.command_builder import build_command
from commands.router import route_command

_RESPONSES_FILE = os.path.join(
    os.path.dirname(__file__), "..", "config", "responses.json"
)

try:
    with open(_RESPONSES_FILE, encoding="utf-8") as f:
        _RESPONSES = json.load(f)
except Exception:
    _RESPONSES = {}


def _random_response(intent: str, fallback: str) -> str | None:
    options = _RESPONSES.get(intent)
    if options:
        return random.choice(options)
    return None

_WAKE_WORDS = [
    "spotify", "oye spotify", "ey spotify", "eh spotify",
    "hey spotify", "hola spotify",
]


def _strip_wake_word(text: str) -> str:
    """
    Remove wake word prefix from transcription if present.
    """
    lower = text.lower().strip()
    for ww in _WAKE_WORDS:
        if lower.startswith(ww):
            stripped = text[len(ww):].strip().lstrip(",").strip()
            return stripped if stripped else text
    return text


def run_voice_assistant():
    """
    Main real-time assistant loop.
    """
    print("\n🎵 Spotify Voice Assistant listo")
    print("─" * 40)
    print("Habla para dar comandos. Ctrl+C para salir.\n")

    while True:
        try:
            print("\nEscuchando...")

            command_text = listen_command()

            if not command_text:
                continue

            command_text = _strip_wake_word(command_text)

            if not command_text:
                continue

            print(f"\n👤 Usuario: {command_text}")

            parsed = build_command(command_text)
            intent = parsed.get("intent")
            entities = parsed.get("entities", {})

            print(f"🧠 Intent: {intent} | Entidades: {entities}")

            if intent is None:
                response = "No entendí ese comando. ¿Puedes repetirlo?"
                print(f"🤖 Asistente: {response}")
                speak(response)
                continue

            response = route_command(intent, entities)

            varied = _random_response(intent, response)
            final_response = varied if varied and "{" not in varied else response

            print(f"🤖 Asistente: {final_response}")
            speak(final_response)

        except KeyboardInterrupt:
            print("\n\nAsistente detenido.")
            break

        except Exception as error:
            print(f"\n❌ Error: {error}")
            speak("Lo siento, ocurrió un error.")
