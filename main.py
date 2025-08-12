import cv2
import numpy as np
import threading
import os
import base64
import speech_recognition as sr
from PIL import Image, ImageDraw
from dotenv import load_dotenv
import socket
from typing import Optional, Tuple, Any, Dict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from tts_utils import speak
from config import TTS_ENGINE, IP_WEBCAM_URL
from scan_logger import log_scan, log_error

# Load Gemini API key from .env
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize LangChain with Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    timeout=None,
    max_retries=2,
    google_api_key=api_key
)

def is_connected() -> bool:
    """Check internet connection status.
    
    Returns:
        bool: True if internet connection is available, False otherwise
    """
    try:
        socket.create_connection(("www.google.com", 80), timeout=2)
        return True
    except OSError as e:
        log_error("No internet connection", {"error": str(e), "type": type(e).__name__})
        return False

# Camera: IP Webcam (phone camera)
cap = cv2.VideoCapture(IP_WEBCAM_URL)

status = "Press 's' or say 'scan' to scan surroundings..."
scan_triggered = False

def process_frame(frame: np.ndarray) -> Tuple[str, bool]:
    """Process a single frame to generate a description."""
    try:
        # Convert frame to RGB for processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        _, buffer = cv2.imencode('.png', frame)
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        
        # Create a message with both text and image for Gemini
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": (
                        "Provide a short, clear, and concise description of this scene "
                        "(1-2 sentences) for a blind person. Focus on key visual elements "
                        "like STOP signs, vehicles, people, or traffic lights."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{encoded_image}"
                },
            ]
        )
        
        # Get response from Gemini via LangChain
        response = llm.invoke([message])
        description = response.content.strip()
        
        log_scan(description, "auto_scan")
        return description, True
        
    except Exception as e:
        error_msg = f"Error processing frame: {str(e)}"
        log_error(error_msg, {
            "error_type": type(e).__name__,
            "frame_shape": frame.shape if frame is not None else None
        })
        return "Unable to analyze the surroundings at the moment.", False

def listen_for_scan() -> None:
    """Continuously listen for voice commands to trigger scanning.
    
    This function runs in a separate thread and updates the global scan_triggered flag
    when the user says 'scan'.
    """
    global scan_triggered
    
    try:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        
        # Adjust for ambient noise
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            log_scan("Microphone calibrated", "system_startup")
            
        log_scan("Voice recognition ready. Listening for 'scan'...", "system_status")
        
        while True:
            try:
                with mic as source:
                    audio = recognizer.listen(
                        source, 
                        timeout=3, 
                        phrase_time_limit=5
                    )
                    
                    command = recognizer.recognize_google(audio).lower()
                    log_scan(f"Heard command: {command}", "voice_command")
                    
                    if "scan" in command:
                        scan_triggered = True
                        log_scan("Scan triggered by voice command", "user_action")
                        
            except sr.WaitTimeoutError:
                # No speech detected, continue listening
                continue
                
            except sr.UnknownValueError:
                # Speech was unintelligible
                log_scan("Could not understand audio", "voice_recognition")
                
            except sr.RequestError as e:
                # API was unreachable or unresponsive
                log_error("Could not request results from speech recognition service", 
                         {"error": str(e)})
                
    except Exception as e:
        log_error("Fatal error in voice recognition thread", 
                 {"error": str(e), "type": type(e).__name__})

def initialize_camera() -> Optional[cv2.VideoCapture]:
    """Initialize and return a camera capture object with error handling."""
    try:
        cap = cv2.VideoCapture(IP_WEBCAM_URL)
        if not cap.isOpened():
            log_error("Failed to open camera", {"camera_url": IP_WEBCAM_URL})
            return None
        return cap
    except Exception as e:
        log_error("Error initializing camera", {
            "error": str(e), 
            "type": type(e).__name__
        })
        return None

def main() -> None:
    """Main application loop."""
    global scan_triggered, status
    
    # Initialize camera
    cap = initialize_camera()
    if cap is None:
        log_error("Could not initialize camera. Exiting.", {"camera_url": IP_WEBCAM_URL})
        speak("Error: Could not connect to the camera. Please check your connection.")
        return

    # Start voice recognition in background
    voice_thread = threading.Thread(target=listen_for_scan, daemon=True)
    voice_thread.start()

    # Check internet connection
    if not is_connected():
        warning_msg = "Warning. You are offline. Scene analysis will not work."
        log_scan(warning_msg, "system_status")
        speak(warning_msg)

    log_scan("Application started successfully", "system_startup")

    try:
        while True:
            # Read frame from camera
            ret, frame = cap.read()
            if not ret:
                log_error("Failed to capture frame from camera", {"camera_url": IP_WEBCAM_URL})
                status = "Camera error. Check your IP Webcam app and Wi-Fi."
                speak("Camera error. Please check your connection.")
                cv2.waitKey(2000)  # Wait before trying again
                continue

            # Display status on frame
            cv2.putText(frame, status, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("VisionMate - Press 'q' to quit", frame)
            
            # Check for key press
            key = cv2.waitKey(1) & 0xFF

            # Handle scan trigger (key press or voice command)
            if key == ord('s') or scan_triggered:
                scan_triggered = False
                status = "Analyzing surroundings..."
                log_scan("Starting scene analysis", "user_action")
                speak("Analyzing surroundings")
                
                # Process the frame and get description
                desc, success = process_frame(frame)
                
                if success:
                    log_scan(f"Scene analysis complete: {desc}", "scan_result")
                    speak(desc)
                    
                    # Alert on specific signs
                    desc_lower = desc.lower()
                    if "stop sign" in desc_lower or "stop" in desc_lower:
                        alert_msg = "Stop! There's a stop sign."
                        log_scan(alert_msg, "safety_alert")
                        speak(alert_msg)
                    elif "red light" in desc_lower:
                        alert_msg = "Stop. It's a red light."
                        log_scan(alert_msg, "safety_alert")
                        speak(alert_msg)
                    elif "yellow light" in desc_lower:
                        alert_msg = "Caution. Yellow light ahead."
                        log_scan(alert_msg, "safety_alert")
                        speak(alert_msg)
                    elif "green light" in desc_lower:
                        alert_msg = "Green light. You can go."
                        log_scan(alert_msg, "safety_alert")
                        speak(alert_msg)
                
                status = "Press 's' or say 'scan' to scan surroundings..."

            # Exit on 'q' key
            elif key == ord('q'):
                log_scan("User initiated application shutdown", "system_shutdown")
                break

    except KeyboardInterrupt:
        log_scan("Application interrupted by user", "system_shutdown")
    except Exception as e:
        log_error("Unexpected error in main loop", {
            "error": str(e),
            "type": type(e).__name__
        })
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        log_scan("Application shutdown complete", "system_shutdown")

if __name__ == "__main__":
    main()
