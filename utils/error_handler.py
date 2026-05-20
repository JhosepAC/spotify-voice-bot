import functools
from utils.logger import logger
from voice.tts_engine import speak

def global_error_handler(func):
    """
    Decorador para capturar errores de forma global, loggearlos y 
    notificar al usuario por voz si es necesario.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"Error en {func.__name__}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            # Notificación al usuario por voz
            # Podríamos personalizar el mensaje según el tipo de error
            speak("Lo siento, ha ocurrido un error interno.")
            
            return None
    return wrapper

class AssistantError(Exception):
    """Excepción base para errores personalizados del asistente."""
    pass

class SpotifyDeviceError(AssistantError):
    """Se lanza cuando no hay un dispositivo de Spotify activo."""
    pass
