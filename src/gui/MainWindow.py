import tkinter as tk
from tkinter import ttk

def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("My Custom GUI")
    root.geometry("400x300")

    # Create a frame
    frame = ttk.Frame(root)
    frame.pack(pady=20)

    # Create a label
    label = ttk.Label(frame, text="Hello, World!")
    label.pack()

    # Create a button
    button = ttk.Button(frame, text="Click Me!")
    button.pack(pady=10)

    # Run the GUI
    root.mainloop()

# Call the function to create the GUI
create_gui()