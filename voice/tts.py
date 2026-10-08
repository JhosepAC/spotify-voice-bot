"""
Text-to-speech engine using pyttsx3.
Selects the best Spanish voice available.
Engine initializes lazily so import never fails without audio devices.
"""

from typing import Any, Callable, Iterable, Optional, cast

import pyttsx3

from config.settings import TTS_RATE, TTS_VOLUME

_engine: Optional[pyttsx3.Engine] = None


def _init_engine() -> pyttsx3.Engine:
    engine = pyttsx3.init()

    voices = cast(list[Any], engine.getProperty("voices"))
    spanish_voice = None

    for voice in voices:
        lang_obj = getattr(voice, "languages", [])
        lang_iterable = cast(Iterable[object], lang_obj)
        lang_str = " ".join(str(l) for l in lang_iterable).lower()
        name_str = voice.name.lower()

        if "es" in lang_str or "spanish" in name_str or "español" in name_str:
            spanish_voice = voice.id
            break

    if spanish_voice:
        engine.setProperty("voice", spanish_voice)

    engine.setProperty("rate", TTS_RATE)
    engine.setProperty("volume", TTS_VOLUME)
    return engine


def get_engine() -> pyttsx3.Engine:
    """Return the shared engine, creating it on first use."""
    global _engine
    if _engine is None:
        _engine = _init_engine()
    return _engine


def _chunks(text: str) -> list[str]:
    """Split a response into short spoken chunks for abort checks."""
    parts = [p.strip() for p in text.replace("!", ".").replace("?", "?|").split(".")]
    return [p for p in (c.strip(" .|") for c in parts) if p]


def speak(text: str, should_abort: Optional[Callable[[], bool]] = None) -> bool:
    """
    Speak text, checking should_abort between short chunks.

    Returns True when fully spoken, False when aborted or on error.
    """
    if not text:
        return True

    print(f"[TTS] {text}")

    try:
        engine = get_engine()
        for chunk in _chunks(text):
            if should_abort is not None and should_abort():
                try:
                    engine.stop()
                except Exception:
                    pass
                return False
            engine.say(chunk)
            engine.runAndWait()
        return True
    except Exception as e:
        print(f"[TTS] Error: {e}")
        try:
            get_engine().stop()
        except Exception:
            pass
        return False
