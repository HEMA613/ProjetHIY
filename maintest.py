import os, sys, json
import tkinter as tk
from tkinter import messagebox

# BASE_DIR = le dossier où se trouve ce fichier main.py
# Permet de construire des chemins relatifs peu importe où on lance le script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# On ajoute le dossier frontend au PATH Python
# pour que Python trouve manager_dashboard.py et employee_dashboard.py
sys.path.insert(0, os.path.join(BASE_DIR, "frontend"))

# Import des deux dashboards (selon le rôle de l'utilisateur connecté)
from manager_dashboard import ManagerDashboard
from employee_dashboard import EmployeeDashboard

# Import du module backend pour initialiser les données au démarrage
from backend import init_data 

def load_backend_users():
    """
    Charge les utilisateurs depuis les fichiers JSON du backend.
    Cherche les managers dans manager.json et les employés dans employes.json.
    Retourne une liste de dictionnaires unifiés avec les champs :
    username, password, full_name, role, total_days.
    """
    users = []

    # On parcourt les deux fichiers JSON : un pour les managers, un pour les employés
    for path, role in [
        (os.path.join(BASE_DIR, "backend", "data", "manager.json"), "manager"),
        (os.path.join(BASE_DIR, "backend", "data", "employes.json"), "employee"),
    ]:
        # Si le fichier n'existe pas encore, on le saute sans planter
        if not os.path.exists(path):
            continue

        with open(path, "r", encoding="utf-8") as f:
            records = json.load(f)

        for r in records:
            users.append({
                "username":   r.get("email"),       # l'email sert d'identifiant de connexion
                "password":   r.get("password", ""),
                "full_name":  r.get("name"),
                "role":       role,
                # Les employés ont un solde de congés limité, les managers ont 9999 (illimité)
                "total_days": r.get("vacation_balance", 25) if role == "employee" else 9999,
            })
    return users


class LoginForm(tk.Tk):
    """Fenêtre de connexion principale — point d'entrée de l'application."""

    def __init__(self):
        super().__init__()
        self.title("Vacation Manager - Login")
        self.geometry("420x420")
        self.configure(bg="#f0f2f5")
        self.resizable(False, False)  # fenêtre non redimensionnable

        # --- Carte blanche centrée (effet "modal card") ---
        card = tk.Frame(self, bg="white", bd=0, relief="flat")
        card.place(relx=0.5, rely=0.5, anchor="center", width=330, height=360)

        # --- Titre et sous-titre ---
        tk.Label(card, text="Vacation Manager",
                 font=("Segoe UI", 18, "bold"), bg="white").pack(pady=(20, 0))
        tk.Label(card, text="Sign in to manage your time off",
                 font=("Segoe UI", 10), fg="#555", bg="white").pack(pady=(0, 20))

        # --- Champ identifiant (email) ---
        tk.Label(card, text="Email Address", font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=30)
        self.username_entry = tk.Entry(card, font=("Segoe UI", 11), bd=1, relief="solid")
        self.username_entry.pack(padx=30, pady=5, fill="x")

        # --- Champ mot de passe (masqué avec show="*") ---
        tk.Label(card, text="Password", font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=30)
        self.password_entry = tk.Entry(card, font=("Segoe UI", 11), bd=1, relief="solid", show="*")
        self.password_entry.pack(padx=30, pady=5, fill="x")

        # --- Bouton de connexion ---
        tk.Button(card, text="Sign In", font=("Segoe UI", 11, "bold"),
                  bg="#1a73e8", fg="white", activebackground="#1666c4",
                  relief="flat", command=self.login).pack(pady=15, ipadx=10, ipady=5)

        # --- Chargement des utilisateurs depuis le backend ---
        self.users = load_backend_users()



    def demo(self, email, full_name, role, parent):
        """
        Affiche un raccourci cliquable pour remplir automatiquement
        les champs email/mot de passe (utile en démo ou développement).
        """
        frame = tk.Frame(parent, bg="white")
        frame.pack(pady=2)

        label = tk.Label(frame,
                         text=f"{email} — {full_name} ({role})",
                         font=("Segoe UI", 9), fg="#1a73e8", bg="white", cursor="hand2")
        label.pack()
        # Au clic, on remplit automatiquement le formulaire avec cet email
        label.bind("<Button-1>", lambda e: self.autofill(email))

    def autofill(self, email):
        """Remplit les champs de connexion avec l'email choisi et le mot de passe 'demo'."""
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, email)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "demo")

    def login(self):
        """
        Vérifie les identifiants saisis.
        Si corrects → ferme le login et ouvre le dashboard correspondant au rôle.
        Si incorrects → affiche un message d'erreur.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Recherche d'un utilisateur dont l'email ET le mot de passe correspondent
        user = next(
            (u for u in self.users if u["username"] == username and u["password"] == password),
            None  # valeur par défaut si rien trouvé
        )

        if not user:
            messagebox.showerror("Error", "Invalid credentials")
            return
 
        messagebox.showinfo("Success", f"Welcome {user['full_name']}!")
        self.destroy()  # ferme la fenêtre de login

        # Crée une nouvelle fenêtre Tkinter pour le dashboard
        root = tk.Tk()
        if user["role"] == "manager":
            ManagerDashboard(root, user, on_logout=self._restart_login)   # dashboard avec droits admin
        else:
            EmployeeDashboard(root, user, on_logout=self._restart_login)  # dashboard employé standard
        root.mainloop()

    def _restart_login(self):
        app = LoginForm()
        app.mainloop()


if __name__ == "__main__":
    # Point d'entrée : on lance l'app uniquement si on exécute ce fichier directement
    app = LoginForm()
    app.mainloop()
