import cv2
import numpy as np
import threading
import os
import speech_recognition as sr
from PIL import Image
from dotenv import load_dotenv
import socket
import google.generativeai as genai

from tts_utils import speak
from config import TTS_ENGINE, IP_WEBCAM_URL

# Load Gemini API key from .env
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def is_connected():
    try:
        socket.create_connection(("www.google.com", 80), timeout=2)
        return True
    except OSError:
        return False

# Camera: IP Webcam (phone camera)
cap = cv2.VideoCapture(IP_WEBCAM_URL)

status = "Press 's' or say 'scan' to scan surroundings..."
scan_triggered = False

def process_frame(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)
    try:
        response = model.generate_content([
            "Describe the scene for a blind person. Mention key things like STOP signs, people, or traffic lights.",
            pil_image
        ])
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return "Unable to analyze surroundings due to internet issue."

def listen_for_scan():
    global scan_triggered
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Microphone calibrated. Listening for 'scan'...")

    while True:
        with mic as source:
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                command = recognizer.recognize_google(audio).lower()
                if "scan" in command:
                    scan_triggered = True
            except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
                pass

# Start voice recognition in background
voice_thread = threading.Thread(target=listen_for_scan, daemon=True)
voice_thread.start()

if not is_connected():
    speak("Warning. You are offline. Scene analysis will not work.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera error. Check your IP Webcam app and Wi-Fi.")
        continue

    cv2.putText(frame, status, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow("Blind Assist Tool", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') or scan_triggered:
        scan_triggered = False
        status = "Analyzing surroundings..."
        speak("Analyzing surroundings")
        desc = process_frame(frame)
        speak(desc)

        # Alert on specific signs
        if "stop sign" in desc.lower() or "stop" in desc.lower():
            speak("Stop! There's a stop sign.")
        elif "red light" in desc.lower():
            speak("Stop. It's a red light.")
        elif "yellow light" in desc.lower():
            speak("Caution. Yellow light ahead.")
        elif "green light" in desc.lower():
            speak("Green light. You can go.")

        status = "Press 's' or say 'scan' to scan surroundings..."

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
