import speech_recognition as sr
import tkinter as tk
from tkinter import simpledialog
import threading

# Tkinter root harus dibuat di thread utama
root = tk.Tk()
root.withdraw()  # Sembunyikan root window

def listen(callback=None):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300  # Adjust threshold for your environment
    mic = None

    # Coba mendeteksi mikrofon
    try:
        mic = sr.Microphone()
    except OSError:
        print("No microphone found or device not available.")
    
    """Fungsi untuk mendengarkan dan mengenali suara."""
    if mic:
        with mic as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")

            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = recognizer.recognize_google(audio)
                print(f"Recognized: {command}")
                if callback:
                    callback(command)
                return command
            except sr.WaitTimeoutError:
                print("Listening timed out. No voice detected.")
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
            except sr.RequestError:
                print("Could not request results; check your network connection.")
    else:
        print("No microphone found.")

    # Jika tidak ada input suara yang berhasil, fallback ke input teks
    if callback:
        root.after(0, lambda: get_text_input(callback))
    return None

def get_text_input(callback=None):
    """Membuka popup untuk input teks dari pengguna di thread utama."""
    user_input = simpledialog.askstring("Input Required", "Microphone not found or no voice detected. Please type your command:", parent=root)
    
    if user_input:
        print(f"Text input: {user_input}")
        if callback:
            callback(user_input)
        return user_input
    else:
        print("No input provided.")
        if callback:
            callback("No input provided.")
        return "No input provided."

# Fungsi yang akan dipanggil setelah mendeteksi perintah
def handle_command(command):
    print(f"Final Command: {command}")

# Contoh penggunaan
if __name__ == "__main__":
    # Jalankan listen di thread terpisah agar tidak mengganggu mainloop Tkinter
    listener_thread = threading.Thread(target=listen, args=(handle_command,))
    listener_thread.start()

    # Jalankan mainloop tkinter di thread utama
    root.mainloop()
