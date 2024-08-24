import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ..models.user import User, Log
from .AdminPage import AdminPage
from .UserPage import UserPage
import datetime
import socket

import os
os.chdir(os.path.dirname(__file__))

# Set the default directory to the assets folder
default_dir = os.path.join(os.getcwd(), "assets/")

class LoginPage:

    def __init__(self, root, session):
        self.session = session
        self.root = root
        self.root.title("User Login")
        self.root.option_add("*tearOff", False)
        self.root.iconbitmap('assets/check.ico')

        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Set window size to half of the screen size
        window_width = screen_width // 2
        window_height = screen_height // 2

        # Calculate position to center the window
        position_right = screen_width // 4
        position_down = screen_height // 4

        # Set the geometry of the window
        root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Make the app responsive
        self.root.columnconfigure(index=0, weight=1)
        self.root.columnconfigure(index=1, weight=1)
        self.root.columnconfigure(index=2, weight=1)
        self.root.rowconfigure(index=0, weight=1)
        self.root.rowconfigure(index=1, weight=1)
        self.root.rowconfigure(index=2, weight=1)


        # Create a style
        Style = ttk.Style(self.root)
        # Import the tcl file
        self.root.tk.call("source", "assets/forest-dark.tcl")
        Style.theme_use("forest-dark")


        # Create a frame for input widgets
        widgets_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
        widgets_frame.grid(row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
        widgets_frame.columnconfigure(index=0, weight=1)

        # Heading
        head = ttk.Label(widgets_frame, text="Login to your Account", font=("Montserrat", 19, "bold"))
        head.grid(row=0, column=0, padx=5, pady=(10, 10), sticky="w")

        # Username label
        username_label = ttk.Label(widgets_frame, text="Username:", font=("Montserrat SemiBold", 10))
        username_label.grid(row=2, column=0, padx=5, pady=(50, 0), sticky="w")

        # Username entry
        self.username_entry = ttk.Entry(widgets_frame)
        # username_entry.insert(0, "Enter Username")
        self.username_entry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")

        # Password label
        password_label = ttk.Label(widgets_frame, text="Password:", font=("Montserrat SemiBold", 10))
        password_label.grid(row=4, column=0, padx=5, pady=(10, 0), sticky="w")

        # Password entry
        self.password_entry = ttk.Entry(widgets_frame, show="⚫")
        # password_entry.insert(0, "Enter Password")
        self.password_entry.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="ew")

        # Login button with Custom Styles
        Style = ttk.Style()
        Style.configure(style="Custom.TButton", font=("Montserrat Bold", 12), background="#4CAF50", foreground="white")
        
        login_button = ttk.Button(widgets_frame, text="Login", style="Custom.TButton", cursor="hand2", command=self.login, takefocus=True)
        login_button.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

        # Load and display an image
        image = Image.open("assets/login.jpg")
        # image = image.resize((320, 540))
        photo = ImageTk.PhotoImage(image)

        image_label = ttk.Label(root, image=photo)
        image_label.image = photo                # Keep a reference to avoid garbage collection
        image_label.grid(row=0, column=0, sticky="sew", rowspan=2)

        # Sizegrip
        # sizegrip = ttk.Sizegrip(self.root)
        # sizegrip.grid(row=99, column=100, padx=(0, 5), pady=(0, 5))

        self.root.update()
        self.root.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Query the database for the user
        user = self.session.query(User).filter_by(username=username).first()

        if user and user.password == password:
            hostname = socket.gethostname()
            ip_address = str(socket.gethostbyname(hostname))

            log = Log(user_id=user.id, login=datetime.datetime.now(), ip=ip_address)
            self.session.add(log)
            self.session.commit()

            if user.is_admin:
                messagebox.showinfo("Login Successful", "Welcome Admin!")
                self.open_admin_window(user)
                
            else:
                # messagebox.showinfo("Login Successful", "Welcome User! 😀")
                self.open_user_window(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password 🚫")
    
    def open_admin_window(self, user):
        self.root.destroy()
        admin_root = tk.Tk()
        AdminPage(admin_root, self.session, user)

    def open_user_window(self, user):
        self.root.destroy()
        user_root = tk.Tk()
        UserPage(user_root, self.session, user)

    