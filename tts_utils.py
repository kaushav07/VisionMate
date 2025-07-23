"""
TTS utility module to support multiple text-to-speech engines:
- gTTS (online, clearer voice)
- pyttsx3 (offline fallback)

Reads config from config.py
"""

from config import TTS_ENGINE
import pyttsx3
from gtts import gTTS
from playsound import playsound
import tempfile
import os

# Initialize pyttsx3 if selected
if TTS_ENGINE == "pyttsx3":
    engine = pyttsx3.init()

def speak(text):
    print(f"Speaking ({TTS_ENGINE}): {text}")

    if TTS_ENGINE == "pyttsx3":
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"[pyttsx3 Error] {e}")

    elif TTS_ENGINE == "gTTS":
        try:
            tts = gTTS(text=text, lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tts.save(tmp.name)
                playsound(tmp.name)
            os.remove(tmp.name)
        except Exception as e:
            print(f"[gTTS Error] {e}. Falling back to pyttsx3.")
            fallback_speak(text)

def fallback_speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[Fallback pyttsx3 Error] {e}")
