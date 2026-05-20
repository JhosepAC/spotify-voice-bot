import json
import random
import os
from utils.logger import logger

RESPONSES_PATH = os.path.join("config", "responses.json")

class ResponseManager:
    def __init__(self):
        self.responses = self._load_responses()

    def _load_responses(self):
        try:
            with open(RESPONSES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error al cargar plantillas de respuesta: {e}")
            return {}

    def get_response(self, category, **kwargs):
        """
        Obtiene una respuesta aleatoria de una categoría y formatea las variables.
        """
        category_list = self.responses.get(category)
        
        if not category_list:
            logger.warning(f"Categoría de respuesta '{category}' no encontrada.")
            return "Hecho."

        response_template = random.choice(category_list)
        
        try:
            return response_template.format(**kwargs)
        except KeyError as e:
            logger.error(f"Falta variable {e} para la plantilla: {response_template}")
            return response_template

# Instancia global
response_manager = ResponseManager()
