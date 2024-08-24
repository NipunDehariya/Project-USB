import tkinter as tk
from src.gui.LoginPage import LoginPage
from src.models.user import session

def main():

    # Initialize and start the Tkinter main window
    root = tk.Tk()
    LoginPage(root, session)
    # root.mainloop()

if __name__ == "__main__":
    main()