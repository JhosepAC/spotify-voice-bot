from voice.command_listener import (
    listen_command
)
from voice.tts_engine import (
    speak
)
from voice.wake_word import WakeWordDetector

from nlp.command_builder import (
    build_command
)
from commands.router import (
    route_command
)

def run_voice_assistant():
    """
    Main voice assistant loop with Wake Word activation.
    """
    # Inicializar detector (por defecto alexa, se puede cambiar a hey_jarvis)
    wake_detector = WakeWordDetector(model_name="alexa")
    
    while True:
        try:
            # Fase 1: Esperar palabra de activación
            if wake_detector.listen_for_wake_word():
                print("Wake word detected! Listening for command...")
                # Opcional: Sonido de feedback o mensaje corto
                # speak("¿Dime?") 

                # Fase 2: Escuchar el comando de Spotify
                text = listen_command(duration=6)

                if not text:
                    continue

                print(f"Detected: {text}")

                parsed_command = build_command(text)

                intent = parsed_command.get("intent")
                entities = parsed_command.get("entities")

                if not intent:
                    speak("I could not understand")
                    continue

                response = route_command(intent, entities)

                speak(response)

        except Exception as error:
            print(f"Pipeline Error: {error}")
            speak("An error occurred")