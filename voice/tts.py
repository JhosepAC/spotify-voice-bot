"""
Text-to-speech engine using pyttsx3.
Selects the best Spanish voice available.
"""

import pyttsx3


def _init_engine() -> pyttsx3.Engine:
    engine = pyttsx3.init()

    voices = engine.getProperty("voices")
    spanish_voice = None

    for voice in voices:
        lang = getattr(voice, "languages", [])
        lang_str = " ".join(str(l) for l in lang).lower()
        name_str = voice.name.lower()

        if "es" in lang_str or "spanish" in name_str or "español" in name_str:
            spanish_voice = voice.id
            break

    if spanish_voice:
        engine.setProperty("voice", spanish_voice)

    engine.setProperty("rate", 165) 
    engine.setProperty("volume", 1.0)

    return engine


_engine = _init_engine()


def speak(text: str):
    """
    Convert text to speech synchronously.
    """
    if not text:
        return

    print(f"[TTS] {text}")

    try:
        _engine.say(text)
        _engine.runAndWait()
    except Exception as e:
        print(f"[TTS] Error: {e}")
        try:
            _engine.stop()
        except Exception:
            pass
