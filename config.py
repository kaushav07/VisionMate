# config.py
# Select the text-to-speech engine.
# Options:
#   "gTTS"     → uses Google Text-to-Speech (online, clearer)
#   "pyttsx3"  → uses system speech engine (offline, basic)

TTS_ENGINE = "gTTS"  # or "pyttsx3"

# IP Webcam URL ((replace with your phone's IP))
# Make sure your phone and laptop are on the same Wi-Fi
IP_WEBCAM_URL = "http://192.168.29.169:8080/video"