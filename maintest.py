import os, sys, json
import tkinter as tk
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "front-end"))
sys.path.insert(0, os.path.join(BASE_DIR, "frontend", "hemadfront"))

from manager_dashboard import ManagerDashboard
from employee_dashboard import EmployeeDashboard
from backend import init_data


def load_backend_users():
    users = []
    for path, role in [
        (os.path.join(BASE_DIR, "backend", "data", "manager.json"), "manager"),
        (os.path.join(BASE_DIR, "backend", "data", "employes.json"), "employee"),
    ]:
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            records = json.load(f)
        for r in records:
            users.append({
                "username": r.get("email"),
                "password": r.get("password", ""),
                "full_name": r.get("name"),
                "role": role,
                "total_days": r.get("vacation_balance", 25) if role == "employee" else 9999,
            })
    return users

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vacation Manager - Login")
        self.geometry("420x420")
        self.configure(bg="#f0f2f5")
        self.resizable(False, False)

        # --- Center frame (card) ---
        card = tk.Frame(self, bg="white", bd=0, relief="flat")
        card.place(relx=0.5, rely=0.5, anchor="center", width=330, height=360)

        # --- Title ---
        tk.Label(card, text="Vacation Manager", 
                 font=("Segoe UI", 18, "bold"), bg="white").pack(pady=(20, 0))

        tk.Label(card, text="Sign in to manage your time off",
                 font=("Segoe UI", 10), fg="#555", bg="white").pack(pady=(0, 20))

        # --- Username ---
        tk.Label(card, text="Email Address", font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=30)
        self.username_entry = tk.Entry(card, font=("Segoe UI", 11), bd=1, relief="solid")
        self.username_entry.pack(padx=30, pady=5, fill="x")

        # --- Password ---
        tk.Label(card, text="Password", font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=30)
        self.password_entry = tk.Entry(card, font=("Segoe UI", 11), bd=1, relief="solid", show="*")
        self.password_entry.pack(padx=30, pady=5, fill="x")

        # --- Login button ---
        tk.Button(card, text="Sign In", font=("Segoe UI", 11, "bold"),
                  bg="#1a73e8", fg="white", activebackground="#1666c4",
                  relief="flat", command=self.login).pack(pady=15, ipadx=10, ipady=5)

  

        self.users = load_backend_users()
        if not self.users:
            self.demo("john@company.com", "John Manager", "manager", card)
            self.demo("sarah@company.com", "Sarah Employee", "employee", card)
        else:
            for u in self.users:
                self.demo(u["username"], u["full_name"], u["role"], card)

    def demo(self, email, full_name, role, parent):
        frame = tk.Frame(parent, bg="white")
        frame.pack(pady=2)

        label = tk.Label(frame, text=f"{email} — {full_name} ({role})", 
                         font=("Segoe UI", 9), fg="#1a73e8", bg="white", cursor="hand2")
        label.pack()
        label.bind("<Button-1>", lambda e: self.autofill(email))

    def autofill(self, email):
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, email)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "demo")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = next((u for u in self.users if u["username"] == username and u["password"] == password), None)
        if not user:
            messagebox.showerror("Error", "Invalid credentials")
            return

        messagebox.showinfo("Success", f"Welcome {user['full_name']}!")
        self.destroy()

        root = tk.Tk()
        if user["role"] == "manager":
            ManagerDashboard(root, user)
        else:
            EmployeeDashboard(root, user)
        root.mainloop()

if __name__ == "__main__":
    app = LoginForm()
    app.mainloop()
    