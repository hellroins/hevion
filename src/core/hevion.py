import sys
import threading
import requests
import keyboard
from src.core.hevion_text_to_speech import speak_online, speak_offline
from src.core.hevion_speech_recognition import listen
from src.extras.tray_icon import run_tray

class HevionAssistant:
    def __init__(self):
        self.internet_available = self.check_internet()
        if self.internet_available:
            print("Connected to the internet. Using Google TTS...")
            self.speak_function = speak_online
        else:
            print("No internet connection. Using pyttsx3 for offline speech...")
            self.speak_function = speak_offline

        self.listening = False
        self.ctrl_pressed = False  # Track Ctrl key state
        self.listener = None  # Initialize the listener as None

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

    def on_press(self, key):
        """Detect key presses."""
        try:
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.ctrl_pressed = True  # Ctrl is pressed
            elif hasattr(key, 'char') and key.char == '1' and self.ctrl_pressed:
                # If Ctrl + 1 is pressed
                if not self.listening:
                    print("Push-to-Talk Activated: Listening...")
                    self.listening = True
                    command = listen()  # Listen for voice command
                    if command:
                        print(f"You said: {command}")
                        self.handle_command(command)
        except AttributeError:
            pass

    def on_release(self, key):
        """Detect key releases."""
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            self.ctrl_pressed = False  # Ctrl key released
        if hasattr(key, 'char') and key.char == '1' and self.listening:
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

    def start_keyboard_listener(self):
        """Start the keyboard listener in a background thread."""
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()

    def run(self):
        """Run the Hevion Assistant."""
        # Start the keyboard listener in a background thread
        listener_thread = threading.Thread(target=self.start_keyboard_listener)
        listener_thread.daemon = True
        listener_thread.start()

        # Run tray icon
        run_tray()