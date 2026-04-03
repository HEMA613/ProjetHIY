import tkinter as tk
from tkinter import messagebox
from manager_dashboard import ManagerDashboard
from employee_dashboard import EmployeeDashboard


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

        # --- Demo accounts ---
        tk.Label(card, text="Demo Accounts (any password works):",
                 font=("Segoe UI", 9, "bold"), bg="white").pack(pady=(10, 5))

        self.demo("john@company.com", "Manager", card)
        self.demo("sarah@company.com", "Employee", card)

    def demo(self, email, role, parent):
        frame = tk.Frame(parent, bg="white")
        frame.pack(pady=2)

        label = tk.Label(frame, text=f"{email} — {role}", 
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

        # --- Manager login ---
        if username == "john@company.com" and password:
            messagebox.showinfo("Success", "Welcome Manager!")
            self.destroy()
            ManagerDashboard()   # Ouvre le dashboard manager

        # --- Employee login ---
        elif username == "sarah@company.com" and password:
            messagebox.showinfo("Success", "Welcome Employee!")
            self.destroy()
            EmployeeDashboard()  # Ouvre le dashboard employé

        else:
            messagebox.showerror("Error", "Invalid credentials")

if __name__ == "__main__":
    app = LoginForm()
    app.mainloop()