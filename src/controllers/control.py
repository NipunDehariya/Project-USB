import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def disable_usb():
    password_window = tk.Toplevel()
    password_window.title("Enter Password")
    password_window.geometry("300x100")
    password_window.resizable(False, False)
    password_label = tk.Label(password_window, text="Enter Password:")
    password_label.pack()
    password_entry = tk.Entry(password_window, show="*") 
    password_entry.pack()

    def check_password():
        if password_entry.get() == "password":
            subprocess.run([r'block_usb.bat'], text=True)
            messagebox.showinfo("Success", "USB Disabled Successfully")
            password_window.destroy()
        else:
            error_label = tk.Label(password_window, text="Incorrect password")
            # messagebox.showerror("Error", "Incorrect password") 
            password_entry.delete(0, 'end')



    #Move these guys to the gui code
    check_password = tk.Button(password_window, text="Submit", command=check_password)
    check_password.pack()
    error_label = tk.Label(password_window, text="", font=("Arial", 10), bg="red", fg="white")
    error_label.pack()


def enable_usb():
    password_window = tk.Toplevel()
    password_window.title("Enter Password")
    password_window.geometry("300x100")
    password_window.resizable(False, False)
    password_label = tk.Label(password_window, text="Enter Password:")
    password_label.pack()
    password_entry = tk.Entry(password_window, show="*") 
    password_entry.pack()

    def check_password():
        if password_entry.get() == "password":
            subprocess.run([r'unblock_usb.bat'], text=True)
            messagebox.showinfo("Success", "USB Enabled Successfully")
            password_window.destroy()
        else:
            error_label = tk.Label(password_window, text="Incorrect password")
            # messagebox.showerror("Error", "Incorrect password") 
            password_entry.delete(0, 'end')
    
    check_password = tk.Button(password_window, text="Submit", command=check_password)
    check_password.pack()
    error_label = tk.Label(password_window, text="", font=("Arial", 10), bg="red", fg="white")