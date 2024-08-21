# import threading
import tkinter as tk
from src.gui.LoginPage import LoginPage
# from src.controllers import geolocation_server
from src.models.user import session

# def run_server():
#     geolocation_server.run()

def main():

    # Start the server (Location Validation) in a separate thread
    # Daemon ensures the thread will close when the main program exits
    # server_thread = threading.Thread(target=run_server)
    # server_thread.daemon = True                         
    # server_thread.start()

    # Initialize and start the Tkinter main window
    root = tk.Tk()
    login_page = LoginPage(root, session)
    root.mainloop()

if __name__ == "__main__":
    main()