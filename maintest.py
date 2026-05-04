import os
import sys
import tkinter as tk
from tkinter import messagebox

# BASE_DIR = le dossier où se trouve ce fichier main.py
#  Permet de construire des chemins relatifs peu importe où on lance le script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# On ajoute le dossier frontend au PATH Python
# pour que Python trouve manager_dashboard.py et employee_dashboard.py
sys.path.insert(0, os.path.join(BASE_DIR, "frontend"))
# On ajoute aussi le service de gestion des congés.
sys.path.insert(0, os.path.join(BASE_DIR, "frontend", "services"))

# Import des deux dashboards (selon le rôle de l'utilisateur connecté)
from employee_dashboard import EmployeeDashboard
from manager_dashboard import ManagerDashboard
from vacation_service import VacationService


def load_backend_users():
    """Charge les utilisateurs du backend en utilisant VacationService."""
    return VacationService().load_users()


class LoginForm(tk.Tk):
    """
    Fenêtre de connexion principale — point d'entrée de l'application.

    Cette classe gère l'authentification des utilisateurs et lance le dashboard
    approprié selon leur rôle (manager ou employé). Elle hérite de tk.Tk pour
    créer une fenêtre racine Tkinter avec une interface moderne et centrée.
    """

    def __init__(self):
        # Appel du constructeur parent pour initialiser la fenêtre Tkinter
        super().__init__()

        # Configuration de base de la fenêtre
        self.title("Vacation Manager - Login")  # Titre affiché dans la barre
        self.geometry("420x420")  # Dimensions fixes de la fenêtre
        self.configure(bg="#f0f2f5")  # Couleur de fond gris clair
        # Empêche le redimensionnement par l'utilisateur
        self.resizable(False, False)

        # Chargement des utilisateurs depuis le backend pour l'authentification
        # Cette liste est utilisée dans login() pour valider les identifiants
        # ET dans _build() pour créer les boutons de démonstration
        self.users = load_backend_users()

        # Construction de l'interface utilisateur (champs, boutons, etc.)
        self._build()

        # Centrage automatique sur l'écran (à la fin, après construction
        # complète)
        self._center()

    def _center(self):
        """Centre la fenêtre sur l'écran."""
        self.update_idletasks()  # Met à jour la géométrie interne avant calcul
        x = (self.winfo_screenwidth() - 420) // 2
        y = (self.winfo_screenheight() - 420) // 2
        # Application de la nouvelle position
        geom = f"420x420+{x}+{y}"
        self.geometry(geom)

    def _build(self):
        """
        Construit l'interface de connexion avec tous les éléments visuels.

        Utilise un design "modal card" : une carte blanche centrée
        sur fond gris, contenant le formulaire de connexion et les boutons
        de démonstration.
        """
        # Frame externe pour centrer le contenu sur la fenêtre
        outer = tk.Frame(self, bg="#f0f2f5")
        outer.place(relx=0.5, rely=0.5, anchor="center", width=330, height=360)

        # Zone du titre avec texte
        tk.Label(
            outer, text="Vacation Manager", font=("Segoe UI", 18, "bold"), bg="#f0f2f5"
        ).pack(pady=(20, 2))
        tk.Label(
            outer,
            text="Sign in to manage your time off",
            font=("Segoe UI", 10),
            fg="#555",
            bg="#f0f2f5",
        ).pack(pady=(0, 20))

        # Carte blanche contenant le formulaire (effet modal)
        card = tk.Frame(outer, bg="white", bd=0, relief="flat")
        card.pack(fill="x")

        # Champ email avec son label
        tk.Label(card, text="Email Address", font=("Segoe UI", 10), bg="white").pack(
            anchor="w", padx=30
        )
        self.username_entry = tk.Entry(
            card, font=("Segoe UI", 11), bd=1, relief="solid"
        )
        self.username_entry.pack(padx=30, pady=5, fill="x")

        # Champ mot de passe masqué avec son label
        tk.Label(card, text="Password", font=("Segoe UI", 10), bg="white").pack(
            anchor="w", padx=30
        )
        self.password_entry = tk.Entry(
            card, font=("Segoe UI", 11), bd=1, relief="solid", show="*"
        )
        self.password_entry.pack(padx=30, pady=5, fill="x")

        # Bouton de connexion stylisé
        tk.Button(
            card,
            text="Sign In",
            font=("Segoe UI", 11, "bold"),
            bg="#1a73e8",
            fg="white",
            activebackground="#1666c4",
            relief="flat",
            command=self.login,
        ).pack(pady=15, ipadx=10, ipady=5)

    def login(self):
        """
        Valide les identifiants et lance le dashboard approprié.

        Appelée lors du clic sur "Sign In".
        Recherche l'utilisateur et ouvre le dashboard manager ou employé.
        """
        username = self.username_entry.get().strip()  # Récupère email
        password = self.password_entry.get().strip()  # Récupère mot de passe

        # Recherche linéaire de l'utilisateur correspondant
        # Utilise next() avec générateur pour trouver le premier match
        user = next(
            (
                u
                for u in self.users
                if u["username"] == username and u["password"] == password
            ),
            None,  # Retourne None si aucun utilisateur trouvé
        )

        if not user:
            # Affichage d'une boîte de dialogue d'erreur
            messagebox.showerror("Erreur", "Identifiants invalides")
            return

        # Message de succès avec le nom de l'utilisateur
        messagebox.showinfo("Succès", f"Bienvenue {user['full_name']}!")

        # Fermeture de la fenêtre de login
        self.destroy()

        # Création d'une nouvelle fenêtre racine pour le dashboard
        root = tk.Tk()
        if user["role"] == "manager":
            # Instanciation du dashboard manager avec callback de déconnexion
            ManagerDashboard(root, user, on_logout=self._restart_login)
        else:
            # Instanciation du dashboard employé avec callback de déconnexion
            EmployeeDashboard(root, user, on_logout=self._restart_login)

        # Lancement de la boucle principale Tkinter pour le dashboard
        root.mainloop()

    def _restart_login(self):
        """
        Callback appelé lors de la déconnexion depuis un dashboard.

        Cette méthode recrée une nouvelle instance de LoginForm,
        permettant à l'utilisateur de se reconnecter avec un autre compte.
        """
        app = LoginForm()  # Nouvelle instance
        app.mainloop()  # Lancement de la boucle


if __name__ == "__main__":
    # Point d'entrée 
    # directement
    app = LoginForm()
    app.mainloop()
