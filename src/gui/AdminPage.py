import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
# import sv_ttk
from PIL import Image, ImageTk
from ..models.user import User
import datetime
from sqlalchemy.orm.exc import NoResultFound
from ..models.user import Log, User
from ..controllers import control
import subprocess

import os
os.chdir(os.path.dirname(__file__))
default_dir = os.path.join(os.getcwd(), "assets")

class AdminPage():
    def __init__(self, root, session, user):
        super().__init__()
        self.session = session
        self.current_user = user
        self.root = root

        self.root.title("Admin Dashboard")
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
        self.root.iconbitmap('assets/main-icon.ico')
        
        # Use sv_ttk for a more modern look
        ttk.Style(self.root)
        # Import the tcl file
        self.root.tk.call("source", "assets/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        # Create a new style for simple borders
        style = ttk.Style()
        style.configure("Divider.TFrame", borderwidth=1, relief="solid", background="#5e5c5c")

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Sidebar
        sidebar = ttk.Frame(main_frame, width=200, style="SimpleBorder.TFrame")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Sidebar title
        ttk.Label(sidebar, text="Dashboard", style="h1.TLabel", font=('montserrat semibold', 15)).pack(pady=10)

        # Sidebar buttons
        buttons = [
            ("Home", self.show_home),
            ("Analytics", self.show_analytics),
            ("Users", self.show_users),
            ("Project Info.", self.show_settings)
        ]

        for text, command in buttons:
            ttk.Button(sidebar, text=text, command=command, style="Accent.TButton", width=10).pack(pady=5, padx=25, fill=tk.X)

        ttk.Button(sidebar, text="Logout", command=self.logout, style="TButton", width=12).pack(pady=50, padx=25, fill=tk.X)

        # Divider frame
        divider = ttk.Frame(main_frame, style="Divider.TFrame")
        divider.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))

        # Main content area
        self.content = ttk.Frame(main_frame)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initial content
        self.show_home()

    def show_home(self):
        self.clear_content()
        ttk.Label(self.content, text="Welcome to the Admin Dashboard", style="h1.TLabel", font=('montserrat semibold', 14)).pack(pady=10)
        # ttk.Label(self.content, text="Here's an overview of your system:", style="TLabel", font=('montserrat', 12)).pack(pady=15)

        # Sample stats
        num_users = self.session.query(User).filter(User.is_admin == False).count()
        num_admins = self.session.query(User).filter(User.is_admin == True).count()
        stats = [
            ("Total Users", num_users),
            ("Total Admins", num_admins),
            ("Total Activity", "1 Hr. 46 Minutes"),
        ]

        for title, value in stats:
            frame = ttk.Frame(self.content, style="SimpleBorder.TFrame")
            frame.pack(pady=10, padx=20, fill=tk.X)
            ttk.Label(frame, text=title, style="TLabel").pack(side=tk.LEFT, padx=10)
            ttk.Label(frame, text=value, style="h2.TLabel").pack(side=tk.RIGHT, padx=10)

        ttk.Button(self.content, text="Block the USB Ports", command=self.block, style="Toggle.TButton", width=20).pack(pady=10, padx=25, anchor="w")
        ttk.Button(self.content, text="Unblock the USB Ports", command=self.unblock, style="Toggle.TButton", width=20).pack(pady=10, padx=25, anchor="w")
    
    def block(self):
        control.block()
        messagebox.showinfo("Enable USB", "USB Blocked Successfully", parent=self.root)

    def unblock(self):
        control.unblock()
        messagebox.showinfo("Disable USB", "USB Enabled Successfully", parent=self.root)

    def show_analytics(self):
        self.clear_content()
        ttk.Label(self.content, text="Analytics and Logs", style="h1.TLabel", font=('montserrat semibold', 14)).pack(pady=10)
        columns = ("user_id", "login", "logout", "duration", "ip")
        names = ("Username", "Login Time", "Logout Time", "Duration", "IP Address")
        tree = ttk.Treeview(self.content, columns=columns, show='headings')

        for column in columns:
            tree.column(column, width=100)

        for name, column in zip(names, columns):
            tree.heading(column, text=name)
        
        # Insert data
        logs = self.session.query(Log).all()
        for log in logs:
            tree.insert("", "end", values=(log.user.username, log.login, log.logout, log.duration, log.ip))
        
        tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    def show_users(self):
        self.clear_content()
        ttk.Label(self.content, text="User Management", style="h1.TLabel", font=('montserrat semibold', 14)).pack(pady=10)
        
        # Create Treeview
        columns = ("name", "username", "email", "is_admin", "permitted", "permitted_from", "permitted_to", "location")
        tree = ttk.Treeview(self.content, columns=columns, show='headings')
        for column in columns:
            tree.column(column, width=100)
        
        # Define headings
        tree.heading("name", text="Name")
        tree.heading("username", text="Username")
        tree.heading("email", text="Email")
        tree.heading("is_admin", text="Admin")
        tree.heading("permitted", text="Permitted")
        tree.heading("permitted_from", text="Permitted From")
        tree.heading("permitted_to", text="Permitted To")
        tree.heading("location", text="Location")
        
        # Insert data
        users = self.session.query(User).all()
        for user in users:
            location = f"({user.latitude}, {user.longitude})"
            tree.insert("", "end", values=(user.name, user.username, user.email, user.is_admin, user.permitted, user.permitted_from, user.permitted_to, location))
        
        tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Add user button
        ttk.Button(self.content, text="Add User", command=self.add_user_form).pack(pady=10)

    def delete_user(self, user):
        # Delete user from the database
        self.session.delete(user)
        self.session.commit()
        # Refresh the user list
        self.show_users()

    def add_user_form(self):
        self.clear_content()

        ttk.Label(self.content, text="Add User", style="h1.TLabel").pack(pady=20)

        # Create a canvas and a scrollbar -----------------------
        canvas = tk.Canvas(self.content)
        scrollbar = ttk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # -------------------------

        fields = [
            ("Name", "name"),
            ("Username", "username"),
            ("Password", "password"),
            ("Email", "email"),
            ("Is Admin", "is_admin"),
            ("Permitted", "permitted"),
            ("Permitted From", "permitted_from"),
            ("Permitted To", "permitted_to"),
            ("Latitude", "latitude"),
            ("Longitude", "longitude")
        ]

        entries = {}
        for i, (label_text, field_name) in enumerate(fields):
            label = ttk.Label(scrollable_frame, text=f"{label_text}:", style="TLabel")
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ttk.Entry(scrollable_frame)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entries[field_name] = entry

        def add_user():
            user_data = {field_name: entry.get() for field_name, entry in entries.items()}
            new_user = User(**user_data)
            self.session.add(new_user)
            self.session.commit()
            self.show_users()

        ttk.Button(scrollable_frame, text="Add", command=add_user).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def show_settings(self):
        self.clear_content()
        ttk.Label(self.content, text="Project Information", style="h1.TLabel", font=('montserrat semibold', 14)).pack(pady=10)
        image = Image.open("assets/Dev.jpg")
        image = image.resize((510, 270))
        photo = ImageTk.PhotoImage(image)

        # Create a label and display the image
        label = ttk.Label(self.content, image=photo)
        label.image = photo 
        label.pack()

        # Create a frame to hold the buttons
        button_frame = ttk.Frame(self.content)
        button_frame.pack(pady=15, padx=15)

        ttk.Button(button_frame, text="View Project Report", command=self.open_pdf, style="Accent.TButton", width=24).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="GitHub", command=self.open_gh, style="Accent.TButton", width=24).grid(row=0, column=1, padx=5)

    def open_pdf(self):
        pdf_path = os.path.join("assets", "project_report.pdf")
        if os.path.exists(pdf_path):
            os.startfile(pdf_path)
        else:
            print(f"File not found: {pdf_path}")

    def open_gh(self):
        webbrowser.open("https://www.github.com/satvikx/Project-USB")

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def logout(self):
        self.root.destroy()
        logout_time = datetime.datetime.now()

        user_id = self.current_user.id
        if user_id is None:
            raise NoResultFound("No user found with the given username.")

        log_entry = self.session.query(Log).filter_by(user_id=user_id).order_by(Log.login.desc()).limit(1).first()
        login_time = log_entry.login if log_entry else None
        
        # Calculate the duration
        duration = logout_time - login_time
        
        log_entry.logout_time = logout_time
        log_entry.duration = duration
        self.session.commit()
        self.current_user = None

        # Deferred import to avoid circular import error
        from .LoginPage import LoginPage
        login_root = tk.Tk()
        ttk.Style(login_root)
        login_root.tk.call("source", "assets/forest-light.tcl")
    
        LoginPage(login_root, self.session)

if __name__ == "__main__":
    root = tk.Tk()
    session = None  # Replace with your SQLAlchemy session
    user = None  # Replace with the current user object
    app = AdminPage(root, session, user)
    root.mainloop()
