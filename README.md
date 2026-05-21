# Spotify Voice Assistant

Asistente de voz para Spotify que entiende lenguaje natural en español usando:
- **Faster-Whisper** (modelo `medium`) para transcripción de voz — 100% local
- **Ollama + Phi-3** para comprensión de intención (NLU) — 100% local, 0 costo
- **Fallback por reglas** si Ollama no está disponible — sin dependencias extra

---

## Instalación

### 1. Requisitos del sistema
- Python 3.10+
- Windows 10/11 (también funciona en Linux/macOS con ajustes menores en TTS)
- Spotify Premium (necesario para controlar reproducción vía API)
- ~2–3 GB de espacio libre para los modelos

---

### 2. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

---

### 3. Instalar Ollama (IA local gratuita)

Ollama permite correr LLMs localmente sin internet y sin costo.

**Windows / Mac:**
Descarga desde: https://ollama.com/download

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Luego descargar el modelo (solo una vez, ~2.3GB):
```bash
ollama pull phi3
```

Verificar que funciona:
```bash
ollama run phi3 "Hola, ¿qué puedes hacer?"
```

> 💡 **¿PC lenta?** Usa `ollama pull phi3:mini` (1.8GB, más rápido).
> **¿Quieres más precisión?** Usa `ollama pull mistral` o `ollama pull llama3`.
> Cambia `OLLAMA_MODEL` en `.env` según el modelo elegido.

---

### 4. Configurar Spotify API

1. Ve a https://developer.spotify.com/dashboard
2. Crea una nueva app
3. En "Edit Settings", añade `http://127.0.0.1:8888/callback` como Redirect URI
4. Copia el Client ID y Client Secret
5. Crea/edita el archivo `.env`:

```env
SPOTIFY_CLIENT_ID=tu_client_id
SPOTIFY_CLIENT_SECRET=tu_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
OLLAMA_MODEL=phi3
```

---

### 5. Ejecutar

**Primero, asegúrate de que Ollama esté corriendo:**
```bash
ollama serve   # En una terminal separada (si no se inicia automáticamente)
```

**Luego:**
```bash
python main.py
```

La primera vez pedirá autenticación con Spotify en el navegador.

---

## Comandos de ejemplo

| Lo que dices | Acción |
|---|---|
| "Pon Blinding Lights de The Weeknd" | Reproduce esa canción |
| "Ponme algo de Shakira" | Reproduce top de Shakira |
| "Quiero escuchar jazz relajante" | Busca playlist de jazz |
| "Dale pausa" | Pausa |
| "Continúa" / "Sigue" | Reanuda |
| "Pasa esta" / "Siguiente" | Siguiente canción |
| "Regresa" / "La anterior" | Canción anterior |
| "Me gusta esta" / "Agrégala a favoritos" | Like a canción actual |
| "Sube el volumen" | +15% volumen |
| "Baja el volumen" | -15% volumen |
| "Pon el volumen al 40" | Volumen al 40% |

---

## Arquitectura

```
Micrófono
    ↓
VAD (energía adaptativa)  ← detecta cuándo hablas
    ↓
Faster-Whisper (modelo small, CPU)  ← transcribe a texto
    ↓
Ollama Phi-3 (LLM local)  ← entiende la intención + extrae entidades
    ↓  (fallback: clasificador por reglas si Ollama no responde)
Router de comandos
    ↓
Spotipy (Spotify API)  ← ejecuta la acción
    ↓
pyttsx3 TTS  ← responde por voz
```

---

## Ajuste de rendimiento

| Situación | Solución |
|---|---|
| Transcripción lenta | Cambiar `WHISPER_MODEL_SIZE = "base"` en `voice/audio_config.py` |
| NLU lenta | Cambiar a `phi3:mini` en `.env` |
| No detecta bien la voz | Bajar `BASE_ENERGY_THRESHOLD` en `audio_config.py` |
| Corta antes de terminar | Subir `MAX_SILENCE_DURATION` en `audio_config.py` |
| Whisper en español mal | Verificar `WHISPER_LANGUAGE = "es"` |
