import pyttsx3

from config.settings import (
    TTS_RATE,
    TTS_VOLUME
)

engine = pyttsx3.init()

engine.setProperty("rate", TTS_RATE)
engine.setProperty("volume", TTS_VOLUME)


def speak(text):
    print(f"BOT: {text}")

    engine.say(text)
    engine.runAndWait()