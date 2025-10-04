# VisionMate

**VisionMate** is an assistive technology project designed to empower visually impaired individuals by providing smart, real-time guidance for safer and more independent navigation.

## Project Overview

VisionMate uses computer vision, text recognition, and speech tech to help users:  

- Recognize objects and surroundings  
- Read printed or handwritten text out loud  
- Control the system easily with voice commands  
- Get real-time alerts about obstacles  
- Add new features easily in the future  

This is the early development and ideation phase. The repository will include prototypes, research notes, and starter code as the project progresses.

## Features (Planned)

- ✅ Real-time object detection  
- ✅ Text-to-speech to read out text
- ✅ Speech-based user controls  
- ✅ Environment awareness for obstacle detection  
- ✅ Modular architecture for future feature integration

## Technology Stack

| Part                | Technology / Tools                        |
|---------------------|-------------------------------------------|
| Programming Language| Python                                    |
| Computer Vision     | OpenCV, Google Cloud Vision API (planned) |
| Backend Framework   | Flask / Django (to be decided)            |
| Frontend / App      | React.js / Flutter (planned)              |
| Database            | MySQL                                     |
| Accessibility APIs  | Text-to-Speech / Speech-to-Text APIs      |

## How It Works 

Here’s how VisionMate works step-by-step:

1. **Captures Input:**  
   Uses a camera to take live pictures or videos of the surroundings.

2. **Detects Objects:**  
   Uses computer vision to find and identify things like doors, obstacles, signs, etc.

3. **Reads Text:**  
   Uses OCR (Optical Character Recognition) to detect printed or handwritten text.

4. **Speech Processing:**  
   - Converts detected text to speech so the user can hear it.  
   - Listens to user’s voice commands to control the system.

5. **Gives Feedback:**  
   Provides real-time audio alerts about obstacles and text info to help the user move safely.

6. **Modular Design:**  
   Built so new features and better AI can be added later easily.


## Getting Started

> 🚧 **Work in Progress**: Only starter files and prototypes are included at this stage.

### Prerequisites

Before you begin, make sure you have the following installed:
- **Python 3.8 or higher** 🐍
- **Git** for cloning the repository
- **A microphone** for voice commands
- **A webcam or phone camera** for video input
- **Google Gemini API key** (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Step 1: Clone the Repository

```bash
git clone https://github.com/kaushav07/VisionMate.git
cd VisionMate
```

### Step 2: Set Up Virtual Environment

It's highly recommended to use a virtual environment to avoid dependency conflicts.

#### Windows
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (you should see (venv) in your prompt)
```

#### Linux/macOS
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (you should see (venv) in your prompt)
```

### Step 3: Install Dependencies

With your virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```
## Contributing 

We’d love your help! Please see [CONTRIBUTING.md](CONTRIBUTING.md) to learn how you can contribute.

 main
### Step 4: Set Up Environment Variables

You need to configure two environment variables before running the project:

#### Option A: Set Environment Variables Temporarily

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-actual-gemini-api-key-here"
$env:WEBCAM_URL="http://your-phone-ip:8080/video"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-actual-gemini-api-key-here
set WEBCAM_URL=http://your-phone-ip:8080/video
```

**Linux/macOS:**
```bash
export GEMINI_API_KEY="your-actual-gemini-api-key-here"
export WEBCAM_URL="http://your-phone-ip:8080/video"
```

#### Option B: Create a .env File (Recommended)

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env  # Linux/macOS
# OR
echo. > .env  # Windows
```

Add the following content to `.env`:
```env
GEMINI_API_KEY=your-actual-gemini-api-key-here
WEBCAM_URL=http://your-phone-ip:8080/video
```

> ⚠️ **Important**: Replace `your-actual-gemini-api-key-here` with your real Gemini API key and `your-phone-ip` with your device's IP address.

### Step 5: Set Up Webcam Stream

For the webcam URL, you have several options:

1. **Use your phone as a webcam** (recommended):
   - Install an IP camera app like "IP Webcam" (Android) or "EpocCam" (iOS)
   - Connect your phone to the same WiFi network as your computer
   - Start the camera stream and note the URL (usually `http://phone-ip:8080/video`)

2. **Use your computer's built-in webcam**:
   - Set `WEBCAM_URL=0` (for default camera)
   - Or set `WEBCAM_URL=1` (for external camera)

3. **Use a USB webcam**:
   - Connect your webcam and set `WEBCAM_URL=0`

### Step 6: Run the Project

With everything set up, you can now run VisionMate:

```bash
python main.py
```

The application will:
- 🎥 Initialize the camera stream
- 🎤 Set up microphone for voice commands
- 🤖 Connect to Google Gemini AI
- 🔊 Start listening for voice commands

**Voice Commands:**
- Say "scan" to analyze the current scene
- The AI will describe what it sees and speak the description aloud

### Quick Start Summary

Here's the complete setup in one go:

```bash
# Clone and setup
git clone https://github.com/kaushav07/VisionMate.git
cd VisionMate
python -m venv venv
venv\Scripts\activate  # Windows
# OR source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Set environment variables
$env:GEMINI_API_KEY="your-key"  # Windows PowerShell
$env:WEBCAM_URL="http://your-phone-ip:8080/video"

# Run the project
python main.py
```

## Environment Setup (Alternative)

If you prefer a different approach to setting up the environment, here are additional options:

### Using .venv instead of venv
Some developers prefer using `.venv` as the virtual environment name:

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/macOS)
source .venv/bin/activate
```

### Using conda (if you prefer Anaconda)
```bash
# Create conda environment
conda create -n visionmate python=3.8

# Activate environment
conda activate visionmate

# Install requirements
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
=======
## 📄 License

This project is licensed under the [MIT License](LICENSE).