import speech_recognition as sr
from tkinter import simpledialog

def listen(root, callback):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    mic = None

    try:
        mic = sr.Microphone()
    except OSError:
        print("No microphone found or device not available.")

    if mic:
        with mic as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")

            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = recognizer.recognize_google(audio)
                print(f"Recognized: {command}")
                callback(command)  # Menggunakan callback
                return
            except sr.WaitTimeoutError:
                print("Listening timed out. No voice detected.")
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
            except sr.RequestError:
                print("Could not request results; check your network connection.")
    
    root.after(0, lambda: get_text_input(root, callback))  # Menggunakan callback untuk dialog

def get_text_input(root, callback):
    user_input = simpledialog.askstring("Input Required", "Please type your command:", parent=root)

    if user_input:
        print(f"Text input: {user_input}")
        callback(user_input)  # Menggunakan callback
    else:
        print("No input provided.")
        callback("No input provided.")

