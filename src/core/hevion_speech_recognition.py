import speech_recognition as sr


def listen():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300  # Adjust threshold for your environment
    mic = sr.Microphone()
    """Fungsi untuk mendengarkan dan mengenali suara."""
    with mic as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print(f"Recognized: {command}")
            return command
        except sr.WaitTimeoutError:
            print("Listening timed out. No voice detected.")
            return "No voice detected."
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return "Sorry, I did not understand that."
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return "Could not request results, check your network connection."
        except OSError:
            print("No microphone found or device not available.")
            return "No microphone found or device not available."
        return None