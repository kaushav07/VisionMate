import cv2
import pyttsx3
import google.genai as genai
import numpy as np
import threading
import speech_recognition as sr
from PIL import Image
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Global config
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

# Thread-safe scan trigger
scan_triggered = threading.Event()


def speak(text: str) -> None:
    """Speak the given text using TTS."""
    logging.info(f"Speaking: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_gemini_model() -> genai.GenerativeModel:
    """Initialize and return the Gemini model client."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logging.critical("GEMINI_API_KEY environment variable not set.")
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name=MODEL_NAME)


def get_webcam_capture() -> cv2.VideoCapture:
    """Initialize and return the webcam capture object."""
    url = os.environ.get("WEBCAM_URL")
    if not url:
        logging.critical("WEBCAM_URL environment variable not set.")
        raise ValueError("WEBCAM_URL environment variable not set.")
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        logging.critical(f"Failed to open webcam at {url}")
        raise RuntimeError(f"Failed to open webcam at {url}")
    return cap


def process_frame(frame: np.ndarray, model: genai.GenerativeModel) -> str:
    """Process a video frame and return a scene description."""
    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        response = model.generate_content([
            "Provide a short, clear, and concise description of this scene (1–2 sentences) for a blind person. Focus only on key visual elements or signs like STOP signs, vehicles, people, or traffic lights.",
            pil_image
        ])
        description = response.text.strip()
        return description
    except Exception as e:
        logging.error(f"Error processing frame or calling API: {e}")
        return "Sorry, I couldn't analyze the scene."


def listen_for_scan() -> None:
    """Listen for the 'scan' voice command and set the scan_triggered event."""
    recognizer = sr.Recognizer()
    try:
        mic = sr.Microphone()
    except Exception as e:
        logging.critical(f"Microphone initialization failed: {e}")
        os._exit(1)

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        logging.info("Microphone calibrated. Listening for 'scan'...")

    while True:
        with mic as source:
            try:
                logging.info("Listening...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                command = recognizer.recognize_google(audio).lower()
                logging.info(f"Recognized: {command}")
                if "scan" in command:
                    logging.info("Voice command 'scan' detected.")
                    scan_triggered.set()
            except sr.WaitTimeoutError:
                logging.debug("Listening timed out, retrying...")
            except sr.UnknownValueError:
                logging.debug("Could not understand audio.")
            except sr.RequestError as e:
                logging.error(f"Speech recognition service error: {e}")
            except Exception as e:
                logging.critical(f"Voice recognition thread error: {e}")
                os._exit(1)


def main() -> None:
    """Main application loop."""
    model = get_gemini_model()
    cap = get_webcam_capture()
    status = "Press 's' or say 'scan' to scan surroundings..."

    # Start voice recognition in a separate thread
    voice_thread = threading.Thread(target=listen_for_scan, daemon=True)
    voice_thread.start()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logging.error("Camera error. Exiting application.")
                break

            cv2.putText(frame, status, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 0), 2)

            cv2.imshow("Blind Assist Tool", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s') or scan_triggered.is_set():
                scan_triggered.clear()  # reset flag
                status = "Analyzing surroundings..."
                speak("Analyzing surroundings")
                desc = process_frame(frame, model)
                speak(desc)

                # Detect important keywords
                desc_lower = desc.lower()
                if "stop sign" in desc_lower or "stop" in desc_lower:
                    speak("Stop! There's a stop sign.")
                elif "red light" in desc_lower:
                    speak("Stop. It's a red light.")
                elif "yellow light" in desc_lower:
                    speak("Caution. Yellow light ahead.")
                elif "green light" in desc_lower:
                    speak("Green light. You can go.")

                status = "Press 's' or say 'scan' to scan surroundings..."

            elif key == ord('q'):
                break
    except Exception as e:
        logging.critical(f"Fatal error in main loop: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logging.info("Application closed gracefully.")


if __name__ == "__main__":
    main()
