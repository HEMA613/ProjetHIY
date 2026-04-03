import tkinter as tk

class ManagerDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard Manager")
        self.geometry("600x450")
        self.configure(bg="#f2f2f2")

        # --- Titre principal ---
        title = tk.Label(self, text="Bienvenue, John Smith",
                         font=("Arial", 20, "bold"), bg="#f2f2f2")
        title.pack(pady=15)

        subtitle = tk.Label(self, text="Tableau de bord du manager",
                            font=("Arial", 12), fg="#555", bg="#f2f2f2")
        subtitle.pack()

        # --- Carte simple ---
        card = tk.Frame(self, bg="#ffcc80", width=400, height=80)
        card.pack(pady=20)
        card.pack_propagate(False)

        card_label = tk.Label(card, text="2 demandes en attente",
                              font=("Arial", 16, "bold"), bg="#ffcc80")
        card_label.pack(expand=True)

        # --- Section demandes ---
        section = tk.Frame(self, bg="white", width=450, height=250, bd=1, relief="solid")
        section.pack(pady=10)
        section.pack_propagate(False)

        section_title = tk.Label(section, text="Demandes en attente",
                                 font=("Arial", 14, "bold"), bg="white")
        section_title.pack(anchor="w", padx=10, pady=10)

        # Exemple d'une demande
        req = tk.Frame(section, bg="#fff7d6", bd=1, relief="solid")
        req.pack(fill="x", padx=10, pady=5)

        tk.Label(req, text="Sarah Johnson", font=("Arial", 12, "bold"),
                 bg="#fff7d6").pack(anchor="w", padx=10, pady=(5, 0))

        tk.Label(req, text="10 Avril → 12 Avril 2026 — Vacances en famille",
                 font=("Arial", 10), bg="#fff7d6").pack(anchor="w", padx=10)

        tk.Label(req, text="3 jours", font=("Arial", 10, "bold"),
                 bg="#ffeb99").pack(anchor="e", padx=10, pady=5)


if __name__ == "__main__":
    app = ManagerDashboard()
    app.mainloop()