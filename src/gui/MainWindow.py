import tkinter as tk
from tkinter import messagebox
from src.models import User

class MainWindow:
    def __init__(self, session):
        self.session = session
        self.root = tk.Tk()
        self.root.title("User Management")

        # Username entry
        tk.Label(self.root, text="Username:").pack()
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack()

        # Add user button
        btn_add_user = tk.Button(self.root, text="Add User", command=self.add_user)
        btn_add_user.pack()

        # User list
        self.user_list = tk.Listbox(self.root)
        self.user_list.pack()

        # Retrieve users button
        btn_retrieve_users = tk.Button(self.root, text="Retrieve Users", command=self.retrieve_users)
        btn_retrieve_users.pack()

    def add_user(self):
        username = self.entry_username.get()
        if username:
            new_user = User(username=username)
            self.session.add(new_user)
            self.session.commit()
            messagebox.showinfo("Success", "User added successfully!")
        else:
            messagebox.showwarning("Input Error", "Please enter a username.")

    def retrieve_users(self):
        users = self.session.query(User).all()
        self.user_list.delete(0, tk.END)
        for user in users:
            self.user_list.insert(tk.END, user.username)