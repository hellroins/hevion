from gtts import gTTS
import pyttsx3
import platform
import os

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
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
