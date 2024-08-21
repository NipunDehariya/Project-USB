import tkinter as tk
from tkinter import ttk, messagebox
from ..models.user import User
from .AdminPage import AdminPage

class LoginPage:
    def __init__(self, root, session):
        self.session = session
        self.root = root
        self.root.title("USB-Login")
        self.root.option_add("*tearOff", False)

        # Set window size to half of the screen size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        position_right = screen_width // 4
        position_down = screen_height // 4
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Apply a theme for a modern look
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # Customize the styling
        cyberpunk_font = ("Courier New", 15, "bold")  # Default Cyberpunk-style font
        heading_font = ("Courier New",22, "bold")    # Larger font for heading
        text_color = "#FFA500"  # Orange text color
        background_color = "#001219"  # Dark background color

        # Set the background color for the root window
        self.root.configure(bg=background_color)

        # Label style
        style.configure("Cyberpunk.TLabel", foreground=text_color, background=background_color, font=cyberpunk_font)

        # Heading style with larger font
        style.configure("Cyberpunk.Heading.TLabel", foreground=text_color, background=background_color, font=heading_font)

        # Entry style - larger size and black text
        style.configure("Cyberpunk.TEntry", foreground="#000000", background="#333333", font=cyberpunk_font, padding=10)

        # Button style
        style.configure("Cyberpunk.TButton", foreground=text_color, background="#333333", font=cyberpunk_font, padding=10)
        style.map("Cyberpunk.TButton", background=[("active", text_color), ("pressed", text_color)], foreground=[("active", "#000000"), ("pressed", "#000000")])

        # Heading
        head = ttk.Label(self.root, text="Admin/User Login", style="Cyberpunk.Heading.TLabel", anchor="center")
        head.grid(row=0, column=0, padx=10, pady=20, sticky="ew")

        # Username label
        username_label = ttk.Label(self.root, text="Username:", style="Cyberpunk.TLabel")
        username_label.grid(row=1, column=0, padx=10, pady=(20, 0), sticky="w")

        # Username entry - larger and black text
        self.username_entry = ttk.Entry(self.root, style="Cyberpunk.TEntry", width=40)
        self.username_entry.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Password label
        password_label = ttk.Label(self.root, text="Password:", style="Cyberpunk.TLabel")
        password_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

        # Password entry - larger and black text
        self.password_entry = ttk.Entry(self.root, show="●", style="Cyberpunk.TEntry", width=40)
        self.password_entry.grid(row=4, column=0, padx=10, pady=(0, 20), sticky="ew")

        # Login button with cyberpunk style
        login_button = ttk.Button(self.root, text="Login", style="Cyberpunk.TButton", cursor="hand2", command=self.login)
        login_button.grid(row=5, column=0, padx=10, pady=20, sticky="nsew")

        # Make the app responsive
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(5, weight=1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Query the database for the user
        user = self.session.query(User).filter_by(username=username).first()

        if user and user.password == password:
            if user.is_admin:
                messagebox.showinfo("Login Successful", "Welcome Admin!")
                self.open_admin_window()
            else:
                messagebox.showinfo("Login Successful", "Welcome User!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_admin_window(self):
        self.root.destroy()
        admin_root = tk.Tk()
        AdminPage(admin_root, self.session)
