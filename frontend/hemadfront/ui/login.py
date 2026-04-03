import tkinter as tk
from tkinter import messagebox
import json, os
from ui.app import VacationApp

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x200")

        tk.Label(self, text="Username").pack()
        self.username = tk.Entry(self)
        self.username.pack()

        tk.Label(self, text="Password").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=10)

    def load_users(self):
        if os.path.exists("data/users.json"):
            with open("data/users.json") as f:
                return json.load(f)
        return []

    def login(self):
        users = self.load_users()
        for u in users:
            if u["username"] == self.username.get() and u["password"] == self.password.get():
                self.destroy()
                root = tk.Tk()
                VacationApp(root, u)
                root.mainloop()
                return
        messagebox.showerror("Error", "Invalid login")
