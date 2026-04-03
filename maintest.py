#c'est qu'un doissier test ne pas l'effacer
# Ajoute les composant:

import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime, date
import calendar

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x150")

        tk.Label(self, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Simulate authentication (replace with real logic)
        if username == "admin" and password == "password":
            messagebox.showinfo("Success", "Login successful!")
            self.destroy()
            # TODO: call main app
        else:
            messagebox.showerror("Error", "Invalid credentials")

if __name__ == "__main__":
    app = LoginForm()
    app.mainloop()
