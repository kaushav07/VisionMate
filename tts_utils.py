"""
tts_utils.py

Handles Text-to-Speech functionality for the Blind Assist Tool.
Supports both gTTS (online) and pyttsx3 (offline) engines with fallback.

Usage:
- Import the speak() function and call speak("your message")
- Engine can be set in config.py using TTS_ENGINE = "gTTS" or "pyttsx3"

"""

from config import TTS_ENGINE
import pyttsx3
from gtts import gTTS
from pydub import AudioSegment
import winsound
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
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_mp3:
                tts.save(tmp_mp3.name)
                # Convert mp3 to wav
                sound = AudioSegment.from_mp3(tmp_mp3.name)
                tmp_wav = tmp_mp3.name.replace('.mp3', '.wav')
                sound.export(tmp_wav, format="wav")
                winsound.PlaySound(tmp_wav, winsound.SND_FILENAME)
            os.remove(tmp_mp3.name)
            os.remove(tmp_wav)
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
