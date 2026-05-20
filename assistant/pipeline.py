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

from utils.logger import logger
from utils.error_handler import global_error_handler

@global_error_handler
def run_voice_assistant():
    """
    Main voice assistant loop with Wake Word activation.
    """
    logger.info("Iniciando Asistente de Voz de Spotify...")
    
    # Inicializar detector
    wake_detector = WakeWordDetector(model_name="alexa")
    
    while True:
        # Fase 1: Esperar palabra de activación
        if wake_detector.listen_for_wake_word():
            logger.info("Wake word detectada. Escuchando comando...")

            # Fase 2: Escuchar el comando de Spotify
            text = listen_command(duration=6)

            if not text:
                logger.warning("No se detectó audio o transcripción vacía.")
                continue

            logger.info(f"Transcripción: {text}")

            parsed_command = build_command(text)

            intent = parsed_command.get("intent")
            entities = parsed_command.get("entities")

            if not intent:
                logger.info("Intención no reconocida.")
                speak("No he podido entender el comando.")
                continue

            logger.info(f"Intento: {intent} | Entidades: {entities}")
            response = route_command(intent, entities)

            speak(response)