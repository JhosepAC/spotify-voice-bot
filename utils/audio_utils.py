import sounddevice as sd
from utils.logger import logger

def list_audio_devices():
    """
    Lista todos los dispositivos de audio disponibles en el sistema.
    """
    devices = sd.query_devices()
    print("\n--- Dispositivos de Audio Detectados ---")
    for i, device in enumerate(devices):
        input_channels = device.get('max_input_channels', 0)
        output_channels = device.get('max_output_channels', 0)
        
        type_str = ""
        if input_channels > 0:
            type_str += "[ENTRADA] "
        if output_channels > 0:
            type_str += "[SALIDA] "
            
        print(f"ID: {i} | {type_str}{device['name']} (Canales: {input_channels} In / {output_channels} Out)")
    print("----------------------------------------\n")

def get_default_input_device():
    """
    Obtiene el dispositivo de entrada por defecto.
    """
    return sd.default.device[0]

if __name__ == "__main__":
    list_audio_devices()
