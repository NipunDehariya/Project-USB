from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ..models.user import User

import os
os.chdir(os.path.dirname(__file__))

# Set the default directory to the assets folder
default_dir = os.path.join(os.getcwd(), "assets")

class AdminPage:
    def __init__(self, root, session):
        self.session = session
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.option_add("*tearOff", False)
        self.root.geometry("750x550")

        label = ttk.Label(self.root, text="Welcome to the Admin Window!")
        label.pack(pady=20)

        self.root.mainloop()

        