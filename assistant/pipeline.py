"""
Main assistant pipeline.
Orchestrates: wake word -> listen -> NLP -> route -> speak
"""

import random
import time
import json
import os

from voice.command_listener import listen_command
from voice.ducking import audio_ducked
from voice.tts import speak
from nlp.command_builder import build_command
from commands.router import route_command
from config.settings import TELEMETRY_ENABLED
from context.manager import push_turn

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


def _log(text: str, intent, entities: dict, lat: dict, response: str) -> None:
    if not TELEMETRY_ENABLED:
        return
    try:
        from assistant.telemetry import log_turn

        log_turn(
            {
                "text": text,
                "intent": intent,
                "entities": entities,
                "latency_s": lat,
                "response": response,
            }
        )
    except Exception:
        pass


def run_voice_assistant():
    """
    Main real-time assistant loop.
    """
    print("\nSpotify Voice Assistant listo")
    print("-" * 40)
    print("Habla para dar comandos. Ctrl+C para salir.\n")

    while True:
        try:
            print("\nEscuchando...")
            lat = {}

            start = time.perf_counter()
            with audio_ducked():
                command_text = listen_command()
            lat["listen"] = round(time.perf_counter() - start, 2)

            if not command_text:
                continue

            command_text = _strip_wake_word(command_text)

            if not command_text:
                continue

            print(f"\nUsuario: {command_text}")

            start = time.perf_counter()
            parsed = build_command(command_text)
            intent = parsed.get("intent")
            entities = parsed.get("entities", {})
            lat["nlu"] = round(time.perf_counter() - start, 2)

            print(f"Intent: {intent} | Entidades: {entities}")
            push_turn(command_text, intent)

            if intent is None:
                response = "No entendí ese comando. ¿Puedes repetirlo?"
                print(f"Asistente: {response}")
                start = time.perf_counter()
                speak(response)
                lat["tts"] = round(time.perf_counter() - start, 2)
                _log(command_text, None, entities, lat, response)
                continue

            start = time.perf_counter()
            response = route_command(intent, entities)
            lat["route"] = round(time.perf_counter() - start, 2)

            varied = _random_response(intent, response)
            final_response = varied if varied and "{" not in varied else response

            print(f"Asistente: {final_response} | lat={lat}")
            start = time.perf_counter()
            speak(final_response)
            lat["tts"] = round(time.perf_counter() - start, 2)
            _log(command_text, intent, entities, lat, final_response)

        except KeyboardInterrupt:
            print("\n\nAsistente detenido.")
            break

        except Exception as error:
            print(f"\nError: {error}")
            speak("Lo siento, ocurrió un error.")
