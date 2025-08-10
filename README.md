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

Clone the repository and install dependencies:

```bash
git clone https://github.com/kaushav07/VisionMate.git
cd VisionMate
pip install -r requirements.txt
```
## Contributing 

We’d love your help! Please see [CONTRIBUTING.md](CONTRIBUTING.md) to learn how you can contribute.

## 📄 License

This project is licensed under the [MIT License](LICENSE).