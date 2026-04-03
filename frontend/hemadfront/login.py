import tkinter as tk
from tkinter import messagebox
import json, os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
sys.path.insert(0, BASE_DIR)

# ── palette ────────────────────────────────────────────────────
BG      = "#0f172a"
CARD    = "#1e293b"
ACCENT  = "#6366f1"
ACCENT2 = "#818cf8"
FG      = "#f8fafc"
MUTED   = "#94a3b8"
BORDER  = "#334155"
ENTRY   = "#0f172a"


class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des Congés")
        self.geometry("460x520")
        self.configure(bg=BG)
        self.resizable(False, False)

        self._center()
        self._build()

    def _center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 460) // 2
        y = (self.winfo_screenheight() - 520) // 2
        self.geometry(f"460x520+{x}+{y}")

    def _build(self):
        outer = tk.Frame(self, bg=BG)
        outer.place(relx=0.5, rely=0.5, anchor="center", width=380, height=460)

        # Logo / icon area
        tk.Label(outer, text="✦", font=("Georgia", 36), fg=ACCENT, bg=BG).pack(pady=(10, 4))
        tk.Label(outer, text="Gestion des Congés",
                 font=("Georgia", 19, "bold"), fg=FG, bg=BG).pack()
        tk.Label(outer, text="Connectez-vous à votre espace",
                 font=("Helvetica", 10), fg=MUTED, bg=BG).pack(pady=(4, 28))

        card = tk.Frame(outer, bg=CARD, bd=0)
        card.pack(fill="x", padx=0, pady=0)

        # Username
        self._field(card, "Nom d'utilisateur", False)
        self.username_entry = self._entry(card)

        self._spacer(card, 10)

        # Password
        self._field(card, "Mot de passe", False)
        self.password_entry = self._entry(card, show="*")
        self.password_entry.bind("<Return>", lambda e: self._login())

        self._spacer(card, 20)

        # Button
        btn = tk.Button(card, text="Se connecter →",
                        font=("Helvetica", 11, "bold"),
                        bg=ACCENT, fg=FG,
                        activebackground=ACCENT2, activeforeground=FG,
                        relief="flat", cursor="hand2",
                        command=self._login)
        btn.pack(padx=30, fill="x", ipady=9, pady=(0, 25))

        # Hint
        tk.Label(outer, text="Mot de passe pour tous les comptes : azerty",
                 font=("Helvetica", 9), fg=MUTED, bg=BG).pack(pady=(16, 0))

    def _field(self, parent, text, bold):
        w = "bold" if bold else "normal"
        tk.Label(parent, text=text, font=("Helvetica", 10, w),
                 fg=MUTED, bg=CARD, anchor="w").pack(anchor="w", padx=30, pady=(14, 2))

    def _entry(self, parent, show=None):
        e = tk.Entry(parent, font=("Helvetica", 12),
                     bg=ENTRY, fg=FG, insertbackground=FG,
                     relief="flat", bd=0,
                     highlightthickness=1, highlightbackground=BORDER,
                     highlightcolor=ACCENT, show=show)
        e.pack(padx=30, fill="x", ipady=8)
        return e

    def _spacer(self, parent, h):
        tk.Frame(parent, bg=CARD, height=h).pack()

    def _load_users(self):
        path = os.path.join(DATA_DIR, "users.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return []

    def _login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.", parent=self)
            return

        for u in self._load_users():
            if u["username"] == username and u["password"] == password:
                self.destroy()
                self._open(u)
                return

        messagebox.showerror("Erreur", "Identifiants incorrects.", parent=self)

    def _open(self, user):
        root = tk.Tk()
        if user["role"] == "admin":
            from ui.admin_dashboard import AdminDashboard
            AdminDashboard(root, user)
        else:
            from ui.employee_dashboard import EmployeeDashboard
            EmployeeDashboard(root, user)
        root.mainloop()
