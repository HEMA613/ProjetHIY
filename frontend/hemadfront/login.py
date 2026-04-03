# Importation des modules nécessaires pour l'interface graphique Tkinter
import tkinter as tk
from tkinter import messagebox
# Importation des modules pour la gestion des fichiers JSON et du système
import json, os, sys

# Définition du répertoire de base pour ajuster les chemins d'importation
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
sys.path.insert(0, BASE_DIR)

# ── Palette de couleurs pour l'interface ────────────────────────────────────────────────────
# Couleurs de base pour le thème sombre
BG      = "#0f172a"  # Couleur de fond principale
CARD    = "#1e293b"  # Couleur des cartes
ACCENT  = "#6366f1"  # Couleur d'accent (bleu)
ACCENT2 = "#818cf8"  # Couleur d'accent secondaire
FG      = "#f8fafc"  # Couleur du texte principal
MUTED   = "#94a3b8"  # Couleur du texte atténué
BORDER  = "#334155"  # Couleur des bordures
ENTRY   = "#0f172a"  # Couleur de fond des champs de saisie

# Classe principale pour le formulaire de connexion
class LoginForm(tk.Tk):
    # Initialisation de la fenêtre de connexion
    def __init__(self):
        super().__init__()  # Appel du constructeur de Tk
        self.title("Gestion des Congés")  # Titre de la fenêtre
        self.geometry("460x520")  # Taille de la fenêtre
        self.configure(bg=BG)  # Couleur de fond
        self.resizable(False, False)  # Empêche le redimensionnement

        self._center()  # Centre la fenêtre sur l'écran
        self._build()   # Construit l'interface

    # Méthode pour centrer la fenêtre sur l'écran
    def _center(self):
        self.update_idletasks()  # Met à jour les tâches de la fenêtre
        x = (self.winfo_screenwidth()  - 460) // 2  # Position x centrée
        y = (self.winfo_screenheight() - 520) // 2  # Position y centrée
        self.geometry(f"460x520+{x}+{y}")  # Applique la géométrie

    # Méthode pour construire l'interface de connexion
    def _build(self):
        outer = tk.Frame(self, bg=BG)  # Frame externe pour centrer le contenu
        outer.place(relx=0.5, rely=0.5, anchor="center", width=380, height=460)  # Placement centré

        # Zone logo / icône
        tk.Label(outer, text="✦", font=("Georgia", 36), fg=ACCENT, bg=BG).pack(pady=(10, 4))  # Icône
        tk.Label(outer, text="Gestion des Congés",  # Titre principal
                 font=("Georgia", 19, "bold"), fg=FG, bg=BG).pack()
        tk.Label(outer, text="Connectez-vous à votre espace",  # Sous-titre
                 font=("Helvetica", 10), fg=MUTED, bg=BG).pack(pady=(4, 28))

        card = tk.Frame(outer, bg=CARD, bd=0)  # Frame pour la carte de connexion
        card.pack(fill="x", padx=0, pady=0)

        # Champ nom d'utilisateur
        self._field(card, "Nom d'utilisateur", False)  # Label du champ
        self.username_entry = self._entry(card)  # Champ de saisie

        self._spacer(card, 10)  # Espaceur

        # Champ mot de passe
        self._field(card, "Mot de passe", False)  # Label du champ
        self.password_entry = self._entry(card, show="*")  # Champ de saisie masqué
        self.password_entry.bind("<Return>", lambda e: self._login())  # Liaison à la touche Entrée

        self._spacer(card, 20)  # Espaceur

        # Bouton de connexion
        btn = tk.Button(card, text="Se connecter →",
                        font=("Helvetica", 11, "bold"),
                        bg=ACCENT, fg=FG,
                        activebackground=ACCENT2, activeforeground=FG,
                        relief="flat", cursor="hand2",
                        command=self._login)  # Commande de connexion
        btn.pack(padx=30, fill="x", ipady=9, pady=(0, 25))

        # Indice pour le mot de passe
        tk.Label(outer, text="Mot de passe pour tous les comptes : azerty",
                 font=("Helvetica", 9), fg=MUTED, bg=BG).pack(pady=(16, 0))

    # Méthode helper pour créer un label de champ
    def _field(self, parent, text, bold):
        w = "bold" if bold else "normal"  # Définit le poids de la police
        tk.Label(parent, text=text, font=("Helvetica", 10, w),
                 fg=MUTED, bg=CARD, anchor="w").pack(anchor="w", padx=30, pady=(14, 2))

    # Méthode helper pour créer un champ de saisie
    def _entry(self, parent, show=None):
        e = tk.Entry(parent, font=("Helvetica", 12),
                     bg=ENTRY, fg=FG, insertbackground=FG,
                     relief="flat", bd=0,
                     highlightthickness=1, highlightbackground=BORDER,
                     highlightcolor=ACCENT, show=show)  # Champ avec style personnalisé
        e.pack(padx=30, fill="x", ipady=8)
        return e

    # Méthode helper pour créer un espaceur
    def _spacer(self, parent, h):
        tk.Frame(parent, bg=CARD, height=h).pack()  # Frame vide pour l'espacement

    # Méthode pour charger les utilisateurs depuis les fichiers JSON du backend
    def _load_users(self):
        # Charger les données du backend, pas du frontend static.
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))  # Chemin vers la racine
        backend_data = os.path.join(root, "backend", "data")  # Dossier des données backend

        users = []  # Liste des utilisateurs
        for path in [os.path.join(backend_data, "manager.json"), os.path.join(backend_data, "employes.json")]:  # Fichiers à charger
            if os.path.exists(path):  # Vérifie si le fichier existe
                with open(path, encoding="utf-8") as f:  # Ouvre le fichier
                    for u in json.load(f):  # Parcourt les utilisateurs
                        role = "manager" if "manager" in os.path.basename(path) else "employee"  # Détermine le rôle
                        users.append({  # Ajoute l'utilisateur à la liste
                            "username": u.get("email"),
                            "password": u.get("password"),
                            "full_name": u.get("name"),
                            "role": role,
                            "total_days": u.get("vacation_balance", 25) if role == "employee" else 9999,  # Jours de congé
                        })
        return users

    # Méthode pour gérer la connexion
    def _login(self):
        username = self.username_entry.get().strip()  # Récupère le nom d'utilisateur
        password = self.password_entry.get().strip()  # Récupère le mot de passe

        if not username or not password:  # Vérifie si les champs sont remplis
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.", parent=self)
            return

        for u in self._load_users():  # Parcourt les utilisateurs
            if u["username"] == username and u["password"] == password:  # Vérifie les identifiants
                self.destroy()  # Ferme la fenêtre de connexion
                self._open(u)  # Ouvre le tableau de bord approprié
                return

        messagebox.showerror("Erreur", "Identifiants incorrects.", parent=self)  # Erreur si identifiants incorrects

    # Méthode pour ouvrir le tableau de bord selon le rôle
    def _open(self, user):
        root = tk.Tk()  # Nouvelle fenêtre Tk
        if user["role"] == "manager":  # Si manager
            from ui.manager_dashboard import ManagerDashboard  # Import du dashboard manager
            ManagerDashboard(root, user)  # Lance le dashboard manager
        else:  # Si employé
            from ui.employee_dashboard import EmployeeDashboard  # Import du dashboard employé
            EmployeeDashboard(root, user)  # Lance le dashboard employé
        root.mainloop()  # Boucle principale
