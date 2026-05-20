import os
import glob
from pathlib import Path

def cleanup_audio_files(directory=None):
    """
    Elimina archivos temporales de audio (.wav) generados durante la sesión.
    """
    # Si no se especifica directorio, usamos el temporal del sistema o el actual
    search_pattern = "*.wav"
    if directory:
        search_pattern = os.path.join(directory, search_pattern)
    
    # Buscamos tanto los archivos originales como los '_enhanced.wav'
    files = glob.glob(search_pattern)
    # También buscamos en la carpeta temporal de Windows si es necesario
    # Pero por ahora nos enfocamos en los que genera nuestro código
    
    for file_path in files:
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                # print(f"Archivo temporal eliminado: {file_path}")
        except Exception as e:
            print(f"Error al eliminar {file_path}: {e}")

def safe_remove(file_path):
    """
    Elimina un archivo específico de forma segura.
    """
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"No se pudo eliminar el archivo {file_path}: {e}")
