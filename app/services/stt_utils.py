"""
stt_utils.py

Handles Speech-to-Text functionality for the Blind Assist Tool.
Supports both Google Speech Recognition (online) and Vosk (offline) engines with fallback.

Usage:
- Import the stt() function and call stt("your message")
- Engine can be set in config.py using TTS_ENGINE = "gTTS" or "pyttsx3"

"""