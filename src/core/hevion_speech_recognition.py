import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    """Fungsi untuk mendengarkan dan mengenali suara."""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)  # Google Speech API digunakan untuk pengenalan suara
            print(f"You said: {command}")
            return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return "Sorry, I did not understand that."
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "Could not request results"
    except OSError:
        print("No microphone found or device not available.")
        return "No microphone found or device not available."
