# VisionMate

**VisionMate** is an assistive technology project designed to empower visually impaired individuals by providing smart, real-time guidance for safer and more independent navigation.

## Project Overview

VisionMate aims to integrate advanced computer vision, text recognition, and speech technologies to help users:
- Identify objects and surroundings
- Read printed or handwritten text aloud
- Provide real-time feedback through a simple, user-friendly interface

This is the early development and ideation phase. The repository will include prototypes, research notes, and starter code as the project progresses.

## Features (Planned)

✅ Object detection using computer vision  
✅ Text-to-speech functionality  
✅ Speech-based user controls  
✅ Environment awareness for obstacle detection  
✅ Modular architecture for future feature integration  

## Tech Stack

- **Python** – Core backend and computer vision  
- **OpenCV** – Image processing and recognition  
- **Flask / Django** – Backend framework (to be finalized)  
- **React.js / Flutter** – Frontend or app interface  
- **MySQL** – Data storage  
- **Google Cloud Vision API** – (future integration)  
- **Text-to-Speech / Speech-to-Text APIs** – Accessibility tools

## Getting Started

> 🚧 **Work in Progress**: Only starter files and prototypes are included at this stage.

Clone the repository and install dependencies:

```bash
git clone https://github.com/kaushav07/VisionMate.git
cd VisionMate
pip install -r requirements.txt
```

### ⚠️ Set Environment Variables
Before running the app, set your Gemini API key and webcam URL as environment variables:

**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-gemini-api-key"
$env:WEBCAM_URL="http://your-phone-ip:8080/video"
python VisionMate/main.py
```

**On Linux/macOS:**
```bash
export GEMINI_API_KEY="your-gemini-api-key"
export WEBCAM_URL="http://your-phone-ip:8080/video"
python VisionMate/main.py
```

Replace the values with your actual API key and webcam stream URL.

## Creating a Python Virtual Environment

It is recommended to use a virtual environment to manage dependencies and avoid conflicts with system packages.

### Windows
```powershell
# Create a virtual environment named .venv
python -m venv .venv
# Activate the virtual environment
.venv\Scripts\activate
```

### Linux/macOS
```bash
# Create a virtual environment named .venv
python3 -m venv .venv
# Activate the virtual environment
source .venv/bin/activate
```

Once activated, install the requirements:
```bash
pip install -r requirements.txt
```

## Troubleshooting: PyAudio Installation Issues

PyAudio is required for microphone access with SpeechRecognition, but it can be difficult to install, especially on Windows.

### Windows Installation
If you get errors installing `pyaudio` with pip, try using [pipwin](https://github.com/lepisma/pipwin), which helps install precompiled Windows binaries:

```powershell
pip install pipwin
pipwin install pyaudio
```

### Linux/macOS Installation
You may need to install portaudio development headers first:

```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio
# macOS (with Homebrew)
brew install portaudio
pip install pyaudio
```

### Alternative: Use SpeechRecognition with Audio Files Only
If you only need to process prerecorded audio files (not microphone input), you can remove `pyaudio` from `requirements.txt` and avoid these issues.

For more help, see the [SpeechRecognition documentation](https://pypi.org/project/SpeechRecognition/).

## Common Issues & Troubleshooting

### 1. Missing Environment Variables
- **Error:** `GEMINI_API_KEY environment variable not set.` or `WEBCAM_URL environment variable not set.`
- **Solution:** Set the required environment variables as described above before running the app.

### 2. Webcam Not Working
- **Error:** `Camera error. Exiting application.`
- **Solution:**
  - Ensure your phone/webcam is streaming and accessible at the URL set in `WEBCAM_URL`.
  - Double-check the IP address and port.
  - Make sure your computer and phone are on the same network.

### 3. Microphone Not Working / PyAudio Errors
- **Error:** `Microphone initialization failed: ...` or errors about PyAudio/PortAudio.
- **Solution:**
  - See the PyAudio troubleshooting section above for installation help.
  - Ensure your microphone is connected and not in use by another application.

### 4. Gemini API/Network Issues
- **Error:** `Error processing frame or calling API: ...`
- **Solution:**
  - Check your internet connection.
  - Make sure your Gemini API key is valid and has not expired.
  - If the Gemini API is down, try again later.

### 5. Application Crashes or Freezes
- **Error:** Unhandled exceptions, app window closes unexpectedly.
- **Solution:**
  - Review the error message printed in the terminal for clues.
  - Ensure all dependencies are installed and up to date.
  - Try restarting the app after fixing any issues.

For further help, please open an issue on the project repository or consult the documentation for the relevant libraries.
