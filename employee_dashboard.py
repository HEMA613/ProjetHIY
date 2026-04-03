import tkinter as tk

class EmployeeDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard Employé")
        self.geometry("600x450")
        self.configure(bg="#f2f2f2")

        # --- Titre principal ---
        title = tk.Label(self, text="Bienvenue, Sarah Johnson",
                         font=("Arial", 20, "bold"), bg="#f2f2f2")
        title.pack(pady=15)

        subtitle = tk.Label(self, text="Votre tableau de bord",
                            font=("Arial", 12), fg="#555", bg="#f2f2f2")
        subtitle.pack()

        # --- Carte simple : jours restants ---
        card = tk.Frame(self, bg="#80bfff", width=400, height=80)
        card.pack(pady=20)
        card.pack_propagate(False)

        card_label = tk.Label(card, text="9 jours de congés restants",
                              font=("Arial", 16, "bold"), bg="#80bfff")
        card_label.pack(expand=True)

        # --- Deux petites cartes ---
        small_cards = tk.Frame(self, bg="#f2f2f2")
        small_cards.pack(pady=10)

        # Carte "En attente"
        pending = tk.Frame(small_cards, bg="#fff7d6", width=180, height=70, bd=1, relief="solid")
        pending.grid(row=0, column=0, padx=10)
        pending.pack_propagate(False)

        tk.Label(pending, text="1 en attente",
                 font=("Arial", 14, "bold"), bg="#fff7d6").pack(expand=True)

        # Carte "Approuvés"
        approved = tk.Frame(small_cards, bg="#d6ffd6", width=180, height=70, bd=1, relief="solid")
        approved.grid(row=0, column=1, padx=10)
        approved.pack_propagate(False)

        tk.Label(approved, text="0 approuvé",
                 font=("Arial", 14, "bold"), bg="#d6ffd6").pack(expand=True)

        # --- Section demandes ---
        section = tk.Frame(self, bg="white", width=450, height=200, bd=1, relief="solid")
        section.pack(pady=20)
        section.pack_propagate(False)

        section_title = tk.Label(section, text="Mes demandes",
                                 font=("Arial", 14, "bold"), bg="white")
        section_title.pack(anchor="w", padx=10, pady=10)

        # Exemple d'une demande
        req = tk.Frame(section, bg="#e6f2ff", bd=1, relief="solid")
        req.pack(fill="x", padx=10, pady=5)

        tk.Label(req, text="Demande du 5 Avril 2026",
                 font=("Arial", 12, "bold"), bg="#e6f2ff").pack(anchor="w", padx=10, pady=(5, 0))

        tk.Label(req, text="Du 10 Avril au 12 Avril — 3 jours",
                 font=("Arial", 10), bg="#e6f2ff").pack(anchor="w", padx=10)

        tk.Label(req, text="Statut : En attente",
                 font=("Arial", 10, "bold"), fg="orange", bg="#e6f2ff").pack(anchor="e", padx=10, pady=5)


if __name__ == "__main__":
    app = EmployeeDashboard()
    app.mainloop()