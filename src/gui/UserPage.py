import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ..models.user import User
import webbrowser
import json
import urllib.parse as urlparse

from http.server import BaseHTTPRequestHandler, HTTPServer
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
        self.root.columnconfigure(index=1, weight=1)
        self.root.columnconfigure(index=2, weight=1)
        self.root.rowconfigure(index=0, weight=1)
        self.root.rowconfigure(index=1, weight=1)
        self.root.rowconfigure(index=2, weight=1)


        # Create a style
        ttk.Style(self.root)
        # Import the tcl file
        self.root.tk.call("source", "assets/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")


        # Create a frame for input widgets
        widgets_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
        widgets_frame.grid(row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
        widgets_frame.columnconfigure(index=0, weight=1)

        label = ttk.Label(widgets_frame, text="Welcome to the User Window!", justify="center")
        label.grid(row=1, column=0, pady=10, columnspan=2)

        # Button
        button = ttk.Button(widgets_frame, text="Enable USB", command=self.check_permissions)           # Add Command to enable the usb
        button.grid(row=2, column=0, padx=5, pady=10, sticky="nsew") 


                        # LOGS
        
        
        # Panedwindow
        label = ttk.Label(widgets_frame, text="User Logs", justify="center")
        label.grid(row=0, column=2, pady=10, columnspan=2)

        paned = ttk.PanedWindow(root)
        paned.grid(row=1, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

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
        treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, columns=(1, 2), height=12)
        treeview.pack(expand=True, fill="both")
        treeScroll.config(command=treeview.yview)

        # Treeview columns
        treeview.column("#0", width=120)
        treeview.column(1, anchor="w", width=120)
        treeview.column(2, anchor="w", width=120)

        # Treeview headings
        treeview.heading("#0", text="Column 1", anchor="center")
        treeview.heading(1, text="Column 2", anchor="center")
        treeview.heading(2, text="Column 3", anchor="center")

        self.root.mainloop()

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

        # Set window size to half of the screen size
        window_width = screen_width // 3
        window_height = screen_height // 3

        # Calculate position to center the window
        position_right = screen_width // 3
        position_down = screen_height // 3

        # Set the geometry of the window
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # label = ttk.Label(self.root, text="Check Permissions")
        # label.pack(pady=10)
        self.root.columnconfigure(index=0, weight=1)
        self.root.columnconfigure(index=1, weight=1)
        
        self.root.rowconfigure(index=0, weight=1)
        self.root.rowconfigure(index=1, weight=1)
        self.root.rowconfigure(index=2, weight=1)

        button = ttk.Button(self.root, text="Check Location", width = 20, command=self.fetch_user_location, style="ToggleButton")
        button.grid(row=0, column=0, padx=50,pady=20, sticky='W')
        self.location_tick = ttk.Label(self.root, text="")
        self.location_tick.grid(row=0, column=1, padx=10, pady=7, sticky='W')

        button = ttk.Button(self.root, text="Check Permission", width = 20, command=self.retrieve_permission, style="ToggleButton")
        button.grid(row=1, column=0,padx=50, pady=20, sticky='W')
        self.permission_tick = ttk.Label(self.root, text="")
        self.permission_tick.grid(row=1, column=1,padx=10, pady=7, sticky='W')

        button = ttk.Button(self.root, text="Enable USB", width = 20, style="Accent.TButton", command=self.enable_usb)   # Disabled by default
        button.grid(row=2, column=0, padx=20, pady=10, columnspan=2)
        
        self.location_data = None
        self.user_permission = None
        
        self.root.mainloop()


    # also bring the Username to filter query

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
            self.location_tick.config(text="✔")
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
        # Implement the logic to VALIDATE and enable USB based on permission and location (maybe converted)
        if self.location_data is None:
            messagebox.showerror("Error", "User location not fetched", parent=self.root)
            return

        if self.user_permission is None:
            messagebox.showerror("Error", "User permission not retrieved", parent=self.root)
            return

        # user = self.session.query(User).filter_by(username=self.logged_in_username).first()
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

    # def stop_server(self):
    #     self.httpd.shutdown()