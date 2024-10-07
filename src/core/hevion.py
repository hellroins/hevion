import sys
import threading
import requests
import tkinter as tk
import platform

# Cek platform untuk hotkey
if platform.system() == "Windows":
    import keyboard
elif platform.system() == "Darwin":  # macOS
    from pynput import keyboard as pynput_keyboard
else:
    raise EnvironmentError("Unsupported OS")

from src.core.hevion_text_to_speech import speak_online, speak_offline
from src.core.hevion_speech_recognition import listen
from src.extras.tray_icon import start_tray_icon

class HevionAssistant:
    def __init__(self):
        self.internet_available = self.check_internet()
        if self.internet_available:
            print("Connected to the internet. Using Google TTS...")
            self.speak_function = speak_online
        else:
            print("No internet connection. Using pyttsx3 for offline speech...")
            self.speak_function = speak_offline

        self.listening = False  # Flag to indicate listening state
        self.listener_thread = None  # To hold the reference to the listening thread

        # Ensure microphone is available
        if not self.check_microphone():
            print("No microphone detected. Please connect a microphone.")
            sys.exit(1)

    def check_internet(self):
        """Check if the device is connected to the internet."""
        try:
            response = requests.get("http://www.google.com", timeout=5)
            return response.status_code == 200
        except requests.ConnectionError:
            return False

    def check_microphone(self):
        """Ensure a microphone is connected."""
        try:
            import speech_recognition as sr
            sr.Microphone.list_microphone_names()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def start_listening(self):
        """Start listening for voice commands."""
        if not self.listening:  # Ensure only one listening process is started
            self.listening = True
            print("Push-to-Talk Activated: Listening...")
            command = listen()  # Call the function to listen for voice input
            if command:
                print(f"You said: {command}")
                self.handle_command(command)
            self.listening = False

    def stop_listening(self):
        """Stop listening for voice commands."""
        if self.listening:
            print("Push-to-Talk Deactivated: Stopped Listening.")
            self.listening = False

    def handle_command(self, command):
        """Handle the voice command and generate response."""
        if "hello" in command.lower():
            response = "Hello! How can I assist you today?"
            self.speak_function(response)
        elif "who are you" in command.lower():
            response = "I am Hevion, your personal assistant."
            self.speak_function(response)
        elif "exit" in command.lower():
            response = "Goodbye!"
            self.speak_function(response)
            sys.exit(0)  # Exit application
        else:
            response = "Sorry, I can't help with that."
            self.speak_function(response)

    # Untuk Windows
    def on_press_windows(self, event):
        """Detect when Ctrl+1 is pressed on Windows."""
        if event.name == '1' and keyboard.is_pressed('ctrl'):
            # Start listening when Ctrl + 1 is pressed
            if not self.listening:  # Prevent starting multiple listeners
                self.listener_thread = threading.Thread(target=self.start_listening)
                self.listener_thread.start()

    def on_release_windows(self, event):
        """Detect when Ctrl+1 is released on Windows."""
        if event.name == '1' and not keyboard.is_pressed('ctrl'):
            # Stop listening when Ctrl + 1 is released
            self.stop_listening()

    # Untuk macOS
    def on_press_mac(self, key):
        """Detect when Ctrl+1 is pressed on macOS."""
        try:
            if key == pynput_keyboard.KeyCode.from_char('1') and keyboard.is_pressed('ctrl'):
                if not self.listening:  # Prevent starting multiple listeners
                    self.listener_thread = threading.Thread(target=self.start_listening)
                    self.listener_thread.start()
        except Exception as e:
            print(f"Error: {e}")

    def on_release_mac(self, key):
        """Detect when Ctrl+1 is released on macOS."""
        if key == pynput_keyboard.KeyCode.from_char('1'):
            self.stop_listening()

    def start_keyboard_listener(self):
        """Start the keyboard listener based on OS."""
        if platform.system() == "Windows":
            # Hook for detecting key press and release events
            keyboard.on_press(self.on_press_windows)
            keyboard.on_release(self.on_release_windows)
            keyboard.wait('esc')  # You can change this to any key to exit the program
        elif platform.system() == "Darwin":  # macOS
            with pynput_keyboard.Listener(on_press=self.on_press_mac, on_release=self.on_release_mac) as listener:
                listener.join()

    def run(self):
        """Run the Hevion Assistant."""
        # Start the keyboard listener in a background thread
        listener_thread = threading.Thread(target=self.start_keyboard_listener)
        listener_thread.daemon = True
        listener_thread.start()

        # Buat instance tkinter di main thread
        root = tk.Tk()

        # Sembunyikan GUI saat startup
        root.withdraw()

        # Jalankan tray icon di thread terpisah, passing root tkinter
        start_tray_icon(root)

        # Jalankan mainloop tkinter di main thread
        root.mainloop()

if __name__ == "__main__":
    assistant = HevionAssistant()
    assistant.run()
