import tkinter as tk
from tkinter import messagebox

class LoginWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root, background="#212121")
        self.geometry("200x300")
        self.resizable(False, False)
        self.title("Login")
        self.app = app

        # Username
        self.username_label = tk.Label(self, text="Username", background="#212121", foreground="#ffffff")
        self.username_label.pack(padx=10, pady=15)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(padx=10, pady=15)

        # Password
        self.password_label = tk.Label(self, text="Password", background="#212121", foreground="#ffffff")
        self.password_label.pack(padx=10, pady=15)
        self.password_entry = tk.Entry(self)
        self.password_entry.pack(padx=10, pady=15)

        button = tk.Button(self, text="LOGIN", command=self.check_login)
        button.pack(padx=10, pady=30)
        self.bind("<Return>", self.check_login)

    def check_login(self, event=None):
        try:
            self.app.api.login(self.username_entry.get(), self.password_entry.get())
            self.destroy()
            self.app.showUserScreen()
        except ValueError as e:
            messagebox.showerror("Error", f"{e}")