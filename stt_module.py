import speech_recognition as sr

def listen_for_command():
    """Listens for a single command from the user and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        # Adjust for ambient noise to improve accuracy
        r.adjust_for_ambient_noise(source)
        try:
            # Listen for audio input from the user
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            # Use Google's speech recognition to convert audio to text
            command = r.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            print("No command heard. Please try again.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

# This part allows you to test the file directly
if __name__ == '__main__':
    listen_for_command()
