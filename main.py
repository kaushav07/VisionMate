#!/usr/bin/env python3
"""
VisionMate - Assistive Technology for Visually Impaired Individuals

This application provides real-time computer vision assistance using:
- Google Gemini AI for scene analysis
- Text-to-speech for audio feedback
- Speech recognition for voice commands
- OpenCV for camera handling

Author: VisionMate Team
Version: 1.0.0
"""

import cv2

import pyttsx3
import google.genai as genai

import numpy as np
import threading
import os
import base64

import speech_recognition as sr
from PIL import Image

import os
import logging
import time
import json
from typing import Optional, Dict, List
from dataclasses import dataclass
from pathlib import Path

# Configure logging with better formatting
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

@dataclass
class Config:
    """Configuration class for VisionMate settings."""
    gemini_api_key: str
    webcam_url: str
    gemini_model: str = "gemini-1.5-flash"
    voice_rate: int = 150
    voice_volume: float = 0.9
    camera_fps: int = 30
    scan_cooldown: float = 2.0  # seconds between scans
    confidence_threshold: float = 0.7

class VisionMateError(Exception):
    """Custom exception for VisionMate-specific errors."""
    pass

class TextToSpeech:
    """Enhanced text-to-speech engine with better voice control."""
    
    def __init__(self, rate: int = 150, volume: float = 0.9):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        # Get available voices and set a good default
        voices = self.engine.getProperty('voices')
        if voices:
            # Prefer female voice if available
            for voice in voices:
                if 'female' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            else:
                self.engine.setProperty('voice', voices[0].id)
    
    def speak(self, text: str, priority: bool = False) -> None:
        """Speak text with optional priority (interrupts current speech)."""
        try:
            if priority:
                self.engine.stop()
            logger.info(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {e}")
            print(f"TTS: {text}")  # Fallback to console output

class SpeechRecognizer:
    """Enhanced speech recognition with better error handling."""
    
    def __init__(self, confidence_threshold: float = 0.7):
        self.recognizer = sr.Recognizer()
        self.confidence_threshold = confidence_threshold
        self.microphone = None
        self._initialize_microphone()
    
    def _initialize_microphone(self) -> None:
        """Initialize microphone with error handling."""
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Microphone initialized successfully")
        except Exception as e:
            logger.error(f"Microphone initialization failed: {e}")
            raise VisionMateError(f"Could not initialize microphone: {e}")
    
    def listen_for_command(self, timeout: int = 3) -> Optional[str]:
        """Listen for voice commands with improved recognition."""
        if not self.microphone:
            return None
            
        try:
            with self.microphone as source:
                logger.debug("Listening for voice command...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
                
                # Try multiple recognition services for better accuracy
                command = self._recognize_audio(audio)
                if command:
                    logger.info(f"Recognized command: {command}")
                    return command.lower()
                    
        except sr.WaitTimeoutError:
            logger.debug("Voice recognition timeout")
        except sr.UnknownValueError:
            logger.debug("Could not understand audio")
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
        except Exception as e:
            logger.error(f"Voice recognition error: {e}")
        
        return None
    
    def _recognize_audio(self, audio) -> Optional[str]:
        """Try multiple recognition services."""
        # Try Google Speech Recognition first
        try:
            return self.recognizer.recognize_google(audio)
        except:
            pass
        
        # Fallback to other services if available
        # Add more recognition services here as needed
        return None
=======
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
os.environ["GOOGLE_API_KEY"] = "your api key"

genai.configure(api_key=api_key)
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

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Encode the frame as PNG image (in memory)
    _, buffer = cv2.imencode('.png', frame)

    # Convert the PNG image bytes to a base64-encoded string (required by Gemini)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    pil_image = Image.fromarray(rgb_frame)
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


class SceneAnalyzer:
    """Enhanced scene analysis using Google Gemini AI."""
    
    def __init__(self, config: Config):
        self.config = config
        self.model = self._initialize_gemini()
        self.last_scan_time = 0
        self.scan_count = 0
    
    def _initialize_gemini(self) -> genai.GenerativeModel:
        """Initialize Gemini model with error handling."""
        try:
            genai.configure(api_key=self.config.gemini_api_key)
            model = genai.GenerativeModel(model_name=self.config.gemini_model)
            logger.info(f"Gemini model '{self.config.gemini_model}' initialized")
            return model
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            raise VisionMateError(f"Could not initialize AI model: {e}")
    
    def analyze_scene(self, frame: np.ndarray) -> str:
        """Analyze scene with rate limiting and enhanced prompts."""
        current_time = time.time()
        if current_time - self.last_scan_time < self.config.scan_cooldown:
            return "Please wait before scanning again."
        
        self.last_scan_time = current_time
        self.scan_count += 1
        
        try:
            # Convert frame to RGB for better AI processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            
            # Enhanced prompt for better descriptions
            prompt = self._get_analysis_prompt()
            
            response = self.model.generate_content([prompt, pil_image])
            description = response.text.strip()
            
            logger.info(f"Scene analysis completed (scan #{self.scan_count})")
            return description
            
        except Exception as e:
            logger.error(f"Scene analysis error: {e}")
            return "Sorry, I couldn't analyze the scene right now."
    
    def _get_analysis_prompt(self) -> str:
        """Get enhanced analysis prompt based on scan count."""
        base_prompt = """
        Provide a clear, concise description of this scene for a visually impaired person.
        Focus on:
        - Important safety elements (stop signs, traffic lights, obstacles)
        - People and their activities
        - Spatial layout and navigation cues
        - Text or signs that might be important
        
        Keep the description to 1-2 sentences and be specific about locations and distances.
        """
        
        if self.scan_count == 1:
            return base_prompt + "\n\nThis is the first scan - provide a general overview of the environment."
        else:
            return base_prompt + "\n\nFocus on any changes or new elements since the last scan."

class CameraManager:
    """Enhanced camera management with multiple fallback options."""
    
    def __init__(self, config: Config):
        self.config = config
        self.cap = None
        self._initialize_camera()
    
    def _initialize_camera(self) -> None:
        """Initialize camera with fallback options."""
        camera_options = [
            self.config.webcam_url,
            "0",  # Default camera
            "1",  # External camera
        ]
        
        for camera_option in camera_options:
            try:

                logger.info(f"Trying camera: {camera_option}")
                self.cap = cv2.VideoCapture(camera_option)
                
                if self.cap.isOpened():
                    # Set camera properties for better performance
                    self.cap.set(cv2.CAP_PROP_FPS, self.config.camera_fps)
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    
                    logger.info(f"Camera initialized successfully: {camera_option}")
                    return
                else:
                    self.cap.release()
                    
            except Exception as e:
                logger.warning(f"Failed to initialize camera {camera_option}: {e}")
                if self.cap:
                    self.cap.release()
        
        raise VisionMateError("Could not initialize any camera")
    
    def read_frame(self) -> Optional[np.ndarray]:
        """Read frame with error handling."""
        if not self.cap:
            return None
            
        try:
            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                logger.warning("Failed to read frame from camera")
                return None
        except Exception as e:
            logger.error(f"Camera read error: {e}")
            return None
    
    def release(self) -> None:
        """Release camera resources."""
        if self.cap:
            self.cap.release()
            logger.info("Camera released")

class VisionMate:
    """Main VisionMate application class."""
    
    def __init__(self, config: Config):
        self.config = config
        self.tts = TextToSpeech(config.voice_rate, config.voice_volume)
        self.speech_recognizer = SpeechRecognizer(config.confidence_threshold)
        self.scene_analyzer = SceneAnalyzer(config)
        self.camera_manager = CameraManager(config)
        
        # Threading
        self.scan_triggered = threading.Event()
        self.running = True
        
        # Voice recognition thread
        self.voice_thread = None
        
        logger.info("VisionMate initialized successfully")
    
    def start_voice_recognition(self) -> None:
        """Start voice recognition in background thread."""
        self.voice_thread = threading.Thread(target=self._voice_recognition_loop, daemon=True)
        self.voice_thread.start()
        logger.info("Voice recognition started")
    
    def _voice_recognition_loop(self) -> None:
        """Background loop for voice recognition."""
        while self.running:
            command = self.speech_recognizer.listen_for_command()
            if command and "scan" in command:
                logger.info("Voice command 'scan' detected")
                self.scan_triggered.set()
            time.sleep(0.1)
    
    def run(self) -> None:
        """Main application loop."""
        self.start_voice_recognition()
        
        try:
            self.tts.speak("VisionMate is ready. Press 's' or say 'scan' to analyze your surroundings.")
            
            while self.running:
                frame = self.camera_manager.read_frame()
                if frame is None:
                    logger.error("Failed to read camera frame")
                    break
                
                # Display status on frame
                self._draw_status(frame)
                
                # Show frame
                cv2.imshow("VisionMate - Assistive Technology", frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('s') or self.scan_triggered.is_set():
                    self.scan_triggered.clear()
                    self._perform_scan(frame)
                elif key == ord('q'):
                    break
                elif key == ord('h'):
                    self._show_help()
                
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Application error: {e}")
        finally:
            self._cleanup()
    
    def _perform_scan(self, frame: np.ndarray) -> None:
        """Perform scene analysis and provide feedback."""
        self.tts.speak("Analyzing surroundings...", priority=True)
        
        # Analyze scene
        description = self.scene_analyzer.analyze_scene(frame)
        self.tts.speak(description)
        
        # Check for important safety elements
        self._check_safety_elements(description)
    
    def _check_safety_elements(self, description: str) -> None:
        """Check for important safety elements in the description."""
        desc_lower = description.lower()
        
        safety_alerts = {
            "stop sign": "Stop! There's a stop sign ahead.",
            "red light": "Stop. It's a red light.",
            "yellow light": "Caution. Yellow light ahead.",
            "green light": "Green light. You can proceed.",
            "vehicle": "Vehicle detected. Be careful.",
            "person": "Person detected nearby.",
            "stairs": "Stairs detected. Be careful with your step.",
            "obstacle": "Obstacle detected. Navigate carefully."
        }
        
        for keyword, alert in safety_alerts.items():
            if keyword in desc_lower:
                self.tts.speak(alert, priority=True)
                break
    
    def _draw_status(self, frame: np.ndarray) -> None:
        """Draw status information on the frame."""
        status = "Press 's' or say 'scan' to analyze | 'h' for help | 'q' to quit"
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, (0, 255, 0), 2)
        
        # Add scan counter
        scan_info = f"Scans: {self.scene_analyzer.scan_count}"
        cv2.putText(frame, scan_info, (10, frame.shape[0] - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    def _show_help(self) -> None:
        """Show help information."""
        help_text = """
        VisionMate Help:
        - Press 's' or say 'scan' to analyze surroundings
        - Press 'h' to show this help
        - Press 'q' to quit
        - The AI will describe what it sees and alert you to important safety elements
        """
        self.tts.speak("Help mode activated. " + help_text)
    
    def _cleanup(self) -> None:
        """Clean up resources."""
        self.running = False
        self.camera_manager.release()
        cv2.destroyAllWindows()
        self.tts.speak("VisionMate shutting down. Thank you for using our assistive technology.")
        logger.info("VisionMate shutdown complete")
=======
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

def load_config() -> Config:
    """Load configuration from environment variables."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise VisionMateError("GEMINI_API_KEY environment variable not set")
    
    webcam_url = os.environ.get("WEBCAM_URL", "0")
    
    return Config(
        gemini_api_key=api_key,
        webcam_url=webcam_url,
        gemini_model=os.environ.get("GEMINI_MODEL", "gemini-1.5-flash"),
        voice_rate=int(os.environ.get("VOICE_RATE", "150")),
        voice_volume=float(os.environ.get("VOICE_VOLUME", "0.9")),
        camera_fps=int(os.environ.get("CAMERA_FPS", "30")),
        scan_cooldown=float(os.environ.get("SCAN_COOLDOWN", "2.0")),
        confidence_threshold=float(os.environ.get("CONFIDENCE_THRESHOLD", "0.7"))
    )

def main() -> None:
    """Main entry point."""
    try:
        logger.info("Starting VisionMate...")
        config = load_config()
        
        app = VisionMate(config)
        app.run()
        
    except VisionMateError as e:
        logger.error(f"VisionMate error: {e}")
        print(f"Error: {e}")
        print("Please check your configuration and try again.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
