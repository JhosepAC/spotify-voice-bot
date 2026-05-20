import os
import numpy as np
import openwakeword
from openwakeword.model import Model
import sounddevice as sd

# Configuración básica
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1280  # Tamaño recomendado para openWakeWord (80ms a 16kHz)

# Obtener dispositivo desde .env o usar el por defecto (None)
INPUT_DEVICE = os.getenv("MICROPHONE_ID")
if INPUT_DEVICE:
    INPUT_DEVICE = int(INPUT_DEVICE)

class WakeWordDetector:
    def __init__(self, model_name="alexa", threshold=0.5):
        """
        Detector de Wake Word usando openWakeWord.
        """
        self.model_name = model_name
        self.threshold = threshold
        
        # Cargar el modelo
        self.oww_model = Model(
            wakeword_models=[model_name],
            inference_framework="onnx"
        )
        
        print(f"WakeWordDetector: Modelo '{model_name}' cargado.")

    def listen_for_wake_word(self):
        """
        Escucha continuamente hasta detectar la palabra de activación.
        """
        print(f"Esperando palabra de activación '{self.model_name}'...")
        
        # Buffer para procesar el audio
        with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype='int16', device=INPUT_DEVICE) as stream:
            while True:
                try:
                    # Leer chunk de audio
                    audio_chunk, overflowed = stream.read(CHUNK_SIZE)
                    
                    # Convertir a array de numpy 1D (aplanar) y procesar
                    # sounddevice devuelve (CHUNK_SIZE, CHANNELS), necesitamos (CHUNK_SIZE,)
                    self.oww_model.predict(audio_chunk.flatten())
                    
                    # Verificar predicciones
                    for mdl in self.oww_model.prediction_buffer.keys():
                        scores = list(self.oww_model.prediction_buffer[mdl])
                        if scores[-1] >= self.threshold:
                            print(f"\n[!] Wake Word Detectada: {mdl}")
                            # Limpiar el estado interno para la próxima vez
                            self.oww_model.reset()
                            return True
                except Exception as e:
                    if "ONNXRuntimeError" in str(e):
                        print(f"Error de Inferencia: {e}")
                        continue
                    raise e

if __name__ == "__main__":
    # Prueba rápida
    detector = WakeWordDetector(model_name="alexa")
    detector.listen_for_wake_word()
