import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ..models.user import User, Log
import webbrowser
import json
import datetime
import urllib.parse as urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy.orm.exc import NoResultFound
from geopy.geocoders import Nominatim
import threading
import os
os.chdir(os.path.dirname(__file__))

# Set the default directory to the assets folder
default_dir = os.path.join(os.getcwd(), "assets")

class UserPage():
    def __init__(self, root, session, user):
        self.session = session
        self.root = root
        self.current_user = user
        self.root.title("User Dashboard")
        self.root.option_add("*tearOff", False)

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
        self.root.columnconfigure(index=1, weight=0)
        self.root.columnconfigure(index=2, weight=1)
        self.root.rowconfigure(index=0, weight=1)
        self.root.rowconfigure(index=1, weight=1)
        self.root.rowconfigure(index=2, weight=1)
        self.root.rowconfigure(index=5, weight=1)

        # Create a style
        ttk.Style(self.root)
        # Import the tcl file
        self.root.tk.call("source", "assets/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        # Create a frame for input widgets
        widgets_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
        widgets_frame.grid(row=0, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=4)

        # Separator Canvas
        separator = tk.Canvas(root, width=2, bg='#5e5c5c', highlightthickness=0)
        separator.grid(row=0, column=1, rowspan=5, sticky="ns")

        label = ttk.Label(widgets_frame, text="USER WINDOW", justify="left", font=('montserrat semibold', 13))
        label.grid(row=0, column=0, pady=(2, 1), columnspan=2)

        # Button for USB Enable
        button = ttk.Button(widgets_frame, text="Enable USB", command=self.check_permissions, width=15)
        button.grid(row=3, column=0, padx=10, pady=(30, 0), sticky="ew")

        # Logout Button
        button = ttk.Button(widgets_frame, text="Logout", style="Accent.TButton", command=self.logout, width=15)
        button.grid(row=4, column=0, padx=10, pady=(20, 2), sticky="ew")

        # User Analytics and Logs Label on the right side
        analytics_label = ttk.Label(root, text="User Analytics and Logs", font=('montserrat', 11))
        analytics_label.grid(row=0, column=2, pady=(40, 2), padx=(20,2), sticky="nsew")

        # Panedwindow
        paned = ttk.PanedWindow(root)
        paned.grid(row=1, column=2, pady=(0, 5), sticky="nsew", rowspan=3)

        # Pane #1
        pane_1 = ttk.Frame(paned)
        paned.add(pane_1, weight=1)

        # Create a Frame for the Treeview
        treeFrame = ttk.Frame(pane_1)
        treeFrame.pack(expand=True, fill="both", padx=5, pady=5)

        # Scrollbar
        treeScroll = ttk.Scrollbar(treeFrame)
        treeScroll.pack(side="right", fill="y")

        # Treeview
        columns = ("user_id", "login", "logout", "duration", "ip")
        names = ("Username", "Login Time", "Logout Time", "Duration", "IP Address")
        tree = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, columns=columns, show='headings', height=12)
        tree.pack(expand=True, fill="both")
        treeScroll.config(command=tree.yview)

        for column in columns:
            tree.column(column, width=100)

        for name, column in zip(names, columns):
            tree.heading(column, text=name)

        logs = self.session.query(Log).join(User).filter(User.is_admin == False).all()
        for log in logs:
            tree.insert("", "end", values=(log.user.username, log.login, log.logout, log.duration, log.ip))

        tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.root.mainloop()

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
        
        # Insert a new record into the Log table
        log_entry.logout_time = logout_time
        log_entry.duration = duration
        self.session.commit()
        self.current_user = None
        self.logged_in_user = None

        # Deferred import to avoid circular import error
        from .LoginPage import LoginPage
        login_root = tk.Tk()
        LoginPage(login_root, self.session)

    def check_permissions(self):
        chk_root = tk.Toplevel(self.root)
        Checks(chk_root, self.session, self.current_user)


class Checks:
    def __init__(self, root, session, user):
        self.session = session
        self.root = root
        self.user = user
        
        self.root.title("Enable USB")
        self.root.option_add("*tearOff", False)
        
        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Set window size to a third of the screen size
        window_width = screen_width // 3
        window_height = screen_height // 3

        # Calculate position to center the window
        position_right = screen_width // 3
        position_down = screen_height // 3

        # Set the geometry of the window
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Separator Canvas
        separator = tk.Canvas(self.root, width=2, bg='#5e5c5c', highlightthickness=0)
        separator.grid(row=0, column=1, rowspan=3, sticky="ns")

        self.root.columnconfigure(index=0, weight=1)
        self.root.columnconfigure(index=1, weight=0)
        self.root.columnconfigure(index=2, weight=1)
        
        self.root.rowconfigure(index=0, weight=1)
        self.root.rowconfigure(index=1, weight=1)
        self.root.rowconfigure(index=2, weight=1)

        button = ttk.Button(self.root, text="Check Location", width=20, command=self.fetch_user_location, style="ToggleButton")
        button.grid(row=0, column=0, padx=50, pady=20, sticky='W')
        self.location_tick = ttk.Label(self.root, text="")
        self.location_tick.grid(row=0, column=1, padx=10, pady=7, sticky='W')

        button = ttk.Button(self.root, text="Check Permission", width=20, command=self.retrieve_permission, style="ToggleButton")
        button.grid(row=1, column=0, padx=50, pady=20, sticky='W')
        self.permission_tick = ttk.Label(self.root, text="")
        self.permission_tick.grid(row=1, column=1, padx=10, pady=7, sticky='W')

        button = ttk.Button(self.root, text="Enable USB", width=20, style="Accent.TButton", command=self.enable_usb)
        button.grid(row=2, column=0, padx=20, pady=10, columnspan=2)
        
        self.location_data = None
        self.user_permission = None
        
        self.root.mainloop()

    def fetch_user_location(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.daemon = True                         
        server_thread.start()

        webbrowser.open('http://localhost:8080/')
        self.poll_location()

    def poll_location(self):
        print("Polling for location data...")
        if self.location_data:
            print("Location data found:", self.location_data)
            messagebox.showinfo("User Location", f"User Location Received : {self.location_data['address']}", parent=self.root)
            self.location_tick.config(text="✅✔️") if self.compare_location() else self.location_tick.config(text="❌")
            return
        else:
            print("no res")
            self.root.after(5000, self.poll_location)  # Poll every 5 seconds

    def retrieve_permission(self):
        if self.user:
            self.user_permission = self.user.permitted
            messagebox.showinfo("User Permission", f"Permission: {self.user_permission}", parent=self.root)
            if self.user_permission:
                self.permission_tick.config(text="✔")
            else:
                self.permission_tick.config(text="❌")
        else:
            messagebox.showerror("Error", "User not found", parent=self.root)

    def enable_usb(self):
        if self.location_data is None:
            messagebox.showerror("Error", "User location not fetched", parent=self.root)
            return

        if self.user_permission is None:
            messagebox.showerror("Error", "User permission not retrieved", parent=self.root)
            return

        if self.user and self.compare_location() and self.user_permission:
            messagebox.showinfo("Enable USB", "USB Enabled Successfully", parent=self.root)
        else:
            messagebox.showerror("Enable USB", "Permission Denied or Location Mismatch", parent=self.root)

    def compare_location(self):
        db_lat = float(self.user.latitude)
        db_lon = float(self.user.longitude)
        lat = float(self.location_data['latitude'])
        lon = float(self.location_data['longitude'])
        print(db_lat, db_lon, lat, lon)

        return round(db_lat, 3) == round(lat, 3) and round(db_lon, 3) == round(lon, 3)

    class LocationHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed_path = urlparse.urlparse(self.path)
            params = urlparse.parse_qs(parsed_path.query)

            if parsed_path.path == '/location' and 'lat' in params and 'lon' in params:
                lat = params['lat'][0]
                lon = params['lon'][0]

                # Store
                geolocator = Nominatim(user_agent="GetLoc")

                # Get address using geopy
                location = geolocator.reverse(f"{lat}, {lon}")

                response = {
                    "address": location.address if location else "Address not found",
                    "latitude": lat,
                    "longitude": lon
                }

                # Send a response back to the browser
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes('{"message": "Location received You can close the Browser"}', "utf-8"))
                self.server.outer_instance.location_data = response

            else:
                # Serve the HTML page
                if parsed_path.path == "/":
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    with open('index.html', 'rb') as file:
                        self.wfile.write(file.read())
                else:
                    self.send_response(404)
                    self.end_headers()

    def run_server(self):
        server_address = ('', 8080)
        self.httpd = HTTPServer(server_address, self.LocationHandler)
        self.httpd.outer_instance = self
        print(f'Starting server on port {8080}...')
        self.httpd.serve_forever()
