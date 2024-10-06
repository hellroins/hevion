import speech_recognition as sr
import pyttsx3
import requests
from gtts import gTTS
import os
import platform

# Inisialisasi recognizer dan engine text-to-speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak_online(text):
    """Fungsi untuk mengeluarkan suara menggunakan gTTS (Google Text-to-Speech)."""
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")

    # Deteksi sistem operasi dan pilih perintah pemutaran audio yang sesuai
    system = platform.system().lower()

    if system == 'windows':
        os.system("start response.mp3")  # Windows
    elif system == 'linux':
        os.system("mpg321 response.mp3")  # Linux
    elif system == 'darwin':  # macOS
        os.system("afplay response.mp3")
    else:
        print("Unsupported OS for audio playback.")
    
def speak_offline(text):
    """Fungsi untuk mengeluarkan suara menggunakan pyttsx3 (Offline TTS)."""
    engine.say(text)
    engine.runAndWait()

def check_internet():
    """Fungsi untuk mengecek apakah ada koneksi internet dengan mencoba mengakses Google."""
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def listen():
    """Fungsi untuk mendengarkan dan mengenali suara."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)  # Google Speech API digunakan untuk pengenalan suara
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

def main():
    """Fungsi utama untuk menjalankan aplikasi."""
    internet_available = False #check_internet()  # Mengecek koneksi internet

    if internet_available:
        print("Connected to the internet. Using Google TTS...")
        speak_function = speak_online
    else:
        print("No internet connection. Using pyttsx3 for offline speech...")
        speak_function = speak_offline

    while True:
        command = listen()  # Mendengarkan perintah suara
        if command:
            if "hello" in command.lower():
                response = "Hello! How can I assist you today?"
                speak_function(response)
            elif "who are you" in command.lower():
                response = "I am Hevion, your personal assistant."
                speak_function(response)
            elif "internet check" in command.lower():
                if internet_available:
                    response = "Internet Available"
                    speak_function(response)
                else:
                    response = "Internet Not Available"
                    speak_function(response)
            elif "exit" in command.lower():
                response = "Goodbye!"
                speak_function(response)
                break
            else:
                response = "Sorry, I can't help with that."
                speak_function(response)

if __name__ == "__main__":
    main()
