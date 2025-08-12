"""
tts_utils.py

Handles Text-to-Speech functionality for the VisionMate application.
Supports both gTTS (online) and pyttsx3 (offline) engines with fallback.

This module provides text-to-speech capabilities with the following features:
- Support for multiple TTS engines (gTTS and pyttsx3)
- Automatic fallback to pyttsx3 if gTTS fails
- Logging of all TTS operations and errors
- Resource cleanup for temporary files

Usage:
    from tts_utils import speak
    speak("Your message here")
"""

import os
import tempfile
from typing import Optional

import pyttsx3
from gtts import gTTS
from playsound import playsound

from config import TTS_ENGINE
from scan_logger import log_scan, log_error

# Initialize pyttsx3 engine if selected
engine: Optional[pyttsx3.Engine] = None
if TTS_ENGINE == "pyttsx3":
    try:
        engine = pyttsx3.init()
        log_scan("Initialized pyttsx3 TTS engine", "system_startup")
    except Exception as e:
        log_error("Failed to initialize pyttsx3 engine", {
            "error": str(e),
            "type": type(e).__name__
        })
        engine = None

def speak(text: str, priority: str = "info") -> bool:
    """Convert text to speech using the configured TTS engine.
    
    Args:
        text: The text to be spoken
        priority: Priority level for logging ('info', 'warning', 'error')
        
    Returns:
        bool: True if speech was successful, False otherwise
    """
    if not text or not isinstance(text, str):
        log_error("Invalid text provided for TTS", {"text": str(text)[:100]})
        return False
        
    log_scan(f"Speaking: {text[:50]}..." if len(text) > 50 else f"Speaking: {text}", 
            f"tts_{TTS_ENGINE.lower()}")
    
    # Use the selected TTS engine
    if TTS_ENGINE == "gTTS":
        return _speak_gtts(text, priority)
    else:  # Default to pyttsx3
        return _speak_pyttsx3(text, priority)

def _speak_gtts(text: str, priority: str) -> bool:
    """Convert text to speech using gTTS (online).
    
    Args:
        text: The text to be spoken
        priority: Priority level for logging
        
    Returns:
        bool: True if speech was successful, False otherwise
    """
    temp_file = None
    try:
        # Create TTS object
        tts = gTTS(text=text, lang='en')
        
        # Create temporary file
        temp_fd, temp_path = tempfile.mkstemp(suffix=".mp3")
        os.close(temp_fd)  # Close the file descriptor as we'll use the path
        temp_file = temp_path
        
        # Save and play
        tts.save(temp_path)
        playsound(temp_path)
        return True
        
    except Exception as e:
        error_msg = f"gTTS Error: {str(e)}"
        log_error(error_msg, {
            "error_type": type(e).__name__,
            "text_length": len(text)
        }, priority)
        
        # Fallback to pyttsx3
        log_scan("Falling back to pyttsx3", "tts_fallback")
        return _speak_pyttsx3(text, priority)
        
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as e:
                log_error("Failed to remove temporary TTS file", {
                    "error": str(e),
                    "file": temp_file
                })

def _speak_pyttsx3(text: str, priority: str) -> bool:
    """Convert text to speech using pyttsx3 (offline).
    
    Args:
        text: The text to be spoken
        priority: Priority level for logging
        
    Returns:
        bool: True if speech was successful, False otherwise
    """
    global engine
    
    # Initialize engine if not already done
    if engine is None:
        try:
            engine = pyttsx3.init()
            log_scan("Initialized pyttsx3 fallback engine", "tts_fallback")
        except Exception as e:
            log_error("Failed to initialize pyttsx3 fallback engine", {
                "error": str(e),
                "type": type(e).__name__
            }, priority)
            return False
    
    # Speak the text
    try:
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception as e:
        log_error("pyttsx3 Error", {
            "error": str(e),
            "type": type(e).__name__,
            "text_length": len(text)
        }, priority)
        return False
