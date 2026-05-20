import logging
import os
from logging.handlers import RotatingFileHandler

# Crear directorio de logs si no existe
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "spotify_bot.log")

def setup_logger():
    """
    Configura un logger centralizado para la aplicación.
    """
    logger = logging.getLogger("SpotifyVoiceBot")
    logger.setLevel(logging.DEBUG)

    # Formato de los logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para consola (Nivel INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Handler para archivo (Nivel DEBUG, con rotación)
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Evitar duplicados si se llama varias veces
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Instancia global del logger
logger = setup_logger()
