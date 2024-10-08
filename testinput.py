import tkinter as tk
from tkinter import simpledialog

# Create the main Tkinter window
root = tk.Tk()
root.title("Customizing tkSimpleDialog.askstring")
root.geometry("720x250")

# Function to show the customized string input dialog
def get_custom_string_input():
   result = simpledialog.askstring(
      "Custom Input", "Enter your name:",
      initialvalue="TutorialsPoint.com"
   )
   if result:
      print("Entered name:", result)

# Create a button to call the get_custom_string_input function
button = tk.Button(
   root, text="Get Custom String Input",
   command=get_custom_string_input
)
button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()