import cv2
import numpy as np
import threading
import os
import base64
import speech_recognition as sr
from PIL import Image
from dotenv import load_dotenv
import socket
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage


from tts_utils import speak
from config import TTS_ENGINE, IP_WEBCAM_URL

# Load Gemini API key from .env
load_dotenv()
api_key = os.getenv("API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    timeout=None,
    max_retries=2,
)

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
    # Convert the OpenCV BGR image to RGB format (PIL expects RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Create a PIL image (not directly used but can be useful for debugging or saving)
    pil_image = Image.fromarray(rgb_frame)

    # Encode the frame as PNG image (in memory)
    _, buffer = cv2.imencode('.png', frame)

    # Convert the PNG image bytes to a base64-encoded string (required by Gemini)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    
    try:
        # Create a HumanMessage for the Gemini model, combining text and image
        message = HumanMessage(
            content=[
                # Text prompt asking for a brief visual description for the blind
                {
                    "type": "text",
                    "text": (
                        "Provide a short, clear, and concise description of this scene "
                        "(1–2 sentences) for a blind person. Focus only on key visual elements "
                        "or signs like STOP signs, vehicles, people, or traffic lights."
                    )
                },
                # Embed the base64 image data as an image input
                {
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{encoded_image}"
                },
            ]
        )

        # Send the prompt to Gemini model using LangChain wrapper and return the description
        response = llm.invoke([message])
        return response.content

    except Exception as e:
        # Print error for debugging and return a fallback message
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
