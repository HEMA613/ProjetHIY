# Importation des modules nécessaires pour l'interface graphique Tkinter
import tkinter as tk
from tkinter import ttk, messagebox
# Importation des modules pour le calendrier, le système et les dates
import calendar, sys, os
from datetime import date

# Définition du répertoire de base pour ajuster les chemins d'importation
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# admin_dashboard est dans frontend/hemadfront, service dans le même dossier sous services
services_dir = os.path.join(BASE_DIR, "hemadfront", "services")
sys.path.insert(0, services_dir)
# Importation du service de gestion des congés
from vacation_service import VacationService

# ── Palette de couleurs pour l'interface ────────────────────────────────────────────────────
# Couleurs de base pour le thème sombre
BG      = "#0f172a"  # Couleur de fond principale
PANEL   = "#1e293b"  # Couleur des panneaux
CARD    = "#263348"  # Couleur des cartes
ACCENT  = "#6366f1"  # Couleur d'accent (bleu)
SUCCESS = "#22c55e"  # Couleur pour le succès (vert)
WARNING = "#f59e0b"  # Couleur pour les avertissements (jaune)
DANGER  = "#ef4444"  # Couleur pour les erreurs (rouge)
FG      = "#f8fafc"  # Couleur du texte principal
MUTED   = "#94a3b8"  # Couleur du texte atténué
BORDER  = "#334155"  # Couleur des bordures

# Configuration des statuts des demandes de congé
STATUS_CFG = {
    "pending":  ("#451a03", "#f59e0b", "⏳ En attente"),  # Statut en attente
    "approved": ("#052e16", "#22c55e", "✅ Approuvé"),   # Statut approuvé
    "rejected": ("#450a0a", "#ef4444", "❌ Refusé"),     # Statut refusé
}

# Fonction helper pour créer des labels avec des paramètres par défaut
def _label(parent, text, size=10, bold=False, fg=FG, bg=None, anchor="w"):
    bg = bg or parent.cget("bg")  # Utilise la couleur de fond du parent si non spécifiée
    w = "bold" if bold else "normal"  # Définit le poids de la police
    return tk.Label(parent, text=text, font=("Helvetica", size, w),
                    fg=fg, bg=bg, anchor=anchor)

# Classe principale pour le tableau de bord du manager (noté admin dans le fichier)
class ManagerDashboard:
    # Initialisation de la classe
    def __init__(self, root, user):
        self.root    = root  # Fenêtre principale Tkinter
        self.user    = user  # Informations de l'utilisateur connecté
        self.service = VacationService()  # Instance du service de congés
        self.cal_year  = date.today().year   # Année actuelle pour le calendrier
        self.cal_month = date.today().month  # Mois actuel pour le calendrier

        # Configuration de la fenêtre
        self.root.title(f"Management — {user['full_name']}")  # Titre de la fenêtre
        self.root.geometry("980x680")  # Taille de la fenêtre
        self.root.configure(bg=BG)  # Couleur de fond
        self.root.resizable(True, True)  # Permet le redimensionnement
        self._center()  # Centre la fenêtre sur l'écran
        self._build()   # Construit l'interface

    # Méthode pour centrer la fenêtre sur l'écran
    def _center(self):
        self.root.update_idletasks()  # Met à jour les tâches de la fenêtre
        x = (self.root.winfo_screenwidth()  - 980) // 2  # Position x centrée
        y = (self.root.winfo_screenheight() - 680) // 2  # Position y centrée
        self.root.geometry(f"980x680+{x}+{y}")  # Applique la géométrie

    # ── Construction de la structure de l'interface ──────────────────────────────────────────────
    def _build(self):
        # Création de l'en-tête
        hdr = tk.Frame(self.root, bg=ACCENT, height=54)  # Frame pour l'en-tête
        hdr.pack(fill="x")  # Étend horizontalement
        hdr.pack_propagate(False)  # Empêche le redimensionnement automatique
        _label(hdr, "✦  Gestion des Congés  ·  Management", 13, True, FG, ACCENT).pack(side="left", padx=22, pady=14)  # Titre à gauche
        _label(hdr, f"👤  {self.user['full_name']}", 10, False, "#c7d2fe", ACCENT).pack(side="right", padx=22)  # Nom de l'utilisateur à droite

        # Configuration du style du notebook (onglets)
        style = ttk.Style()
        style.theme_use("default")  # Utilise le thème par défaut
        style.configure("TNotebook",         background=BG,    borderwidth=0)  # Style du notebook
        style.configure("TNotebook.Tab",     background=PANEL, foreground=MUTED,
                        font=("Helvetica", 10), padding=[18, 8])  # Style des onglets
        style.map("TNotebook.Tab",
                  background=[("selected", CARD)],  # Couleur quand sélectionné
                  foreground=[("selected", FG)])

        # Création du notebook avec les onglets
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=0, pady=0)  # Étend dans toute la fenêtre

        # Création des onglets
        self.tab_req  = tk.Frame(nb, bg=BG); nb.add(self.tab_req,  text="  📋  Demandes  ")  # Onglet Demandes
        self.tab_cal  = tk.Frame(nb, bg=BG); nb.add(self.tab_cal,  text="  📅  Calendrier  ")  # Onglet Calendrier
        self.tab_emp  = tk.Frame(nb, bg=BG); nb.add(self.tab_emp,  text="  👥  Employees  ")  # Onglet Employés

        # Construction des contenus des onglets
        self._build_requests()   # Construit l'onglet Demandes
        self._build_calendar()   # Construit l'onglet Calendrier
        self._build_employees()  # Construit l'onglet Employés

    # ── Construction de l'onglet Demandes ─────────────────────────────────────
    def _build_requests(self):
        # Création de la ligne de statistiques
        stats_row = tk.Frame(self.tab_req, bg=BG)
        stats_row.pack(fill="x", padx=20, pady=(16, 8))  # Étend horizontalement avec marges

        # Récupération de toutes les demandes de congé
        vacs = self.service.get_all_vacations()
        # Création des cartes de statistiques pour chaque statut
        for count, label, color in [
            (len([v for v in vacs if v["status"] == "pending"]),  "En attente", WARNING),  # Nombre en attente
            (len([v for v in vacs if v["status"] == "approved"]), "Approuvés",  SUCCESS),  # Nombre approuvés
            (len([v for v in vacs if v["status"] == "rejected"]), "Refusés",    DANGER),   # Nombre refusés
            (len(vacs),                                           "Total",      ACCENT),   # Total
        ]:
            c = tk.Frame(stats_row, bg=PANEL, bd=0)  # Frame pour chaque statistique
            c.pack(side="left", padx=6, ipadx=22, ipady=10)  # Aligne à gauche
            _label(c, str(count), 26, True, color, PANEL, "center").pack()  # Nombre
            _label(c, label,      9,  False, MUTED, PANEL, "center").pack()  # Label

        # Création de la barre de filtrage
        flt = tk.Frame(self.tab_req, bg=BG)
        flt.pack(fill="x", padx=20, pady=(0, 6))  # Étend horizontalement
        _label(flt, "Filtrer :", 10, False, MUTED, BG).pack(side="left", padx=(0, 10))  # Label "Filtrer :"
        self.filter_var = tk.StringVar(value="all")  # Variable pour le filtre
        # Création des boutons radio pour les filtres
        for val, txt in [("all", "Tous"), ("pending", "En attente"), ("approved", "Approuvés"), ("rejected", "Refusés")]:
            rb = tk.Radiobutton(flt, text=txt, variable=self.filter_var, value=val,
                                command=self._refresh_req,  # Commande pour rafraîchir
                                bg=BG, fg=MUTED, selectcolor=PANEL,
                                activebackground=BG, activeforeground=FG,
                                font=("Helvetica", 10))
            rb.pack(side="left", padx=8)  # Aligne à gauche

        # Configuration du style du Treeview (tableau)
        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background=PANEL, foreground=FG,
                        fieldbackground=PANEL, rowheight=32,
                        font=("Helvetica", 10))  # Style du tableau
        style.configure("Dark.Treeview.Heading",
                        background=CARD, foreground=MUTED,
                        font=("Helvetica", 10, "bold"), relief="flat")  # Style des en-têtes
        style.map("Dark.Treeview", background=[("selected", ACCENT)])  # Couleur de sélection

        # Définition des colonnes du tableau
        cols = ("Employee", "Début", "Fin", "Durée", "Motif", "Soumis le", "Statut")
        frm  = tk.Frame(self.tab_req, bg=BG)
        frm.pack(fill="both", expand=True, padx=20, pady=4)  # Frame pour le tableau

        # Création du Treeview
        self.tree = ttk.Treeview(frm, columns=cols, show="headings",
                                 style="Dark.Treeview", height=14)  # Tableau avec 14 lignes visibles
        widths = [130, 100, 100, 70, 200, 100, 130]  # Largeurs des colonnes
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)  # En-tête de colonne
            self.tree.column(col, width=w, anchor="center")  # Configuration de colonne

        # Configuration des tags pour colorer les lignes selon le statut
        self.tree.tag_configure("pending",  background="#451a03", foreground="#fde68a")  # Couleur pour en attente
        self.tree.tag_configure("approved", background="#052e16", foreground="#86efac")  # Couleur pour approuvé
        self.tree.tag_configure("rejected", background="#450a0a", foreground="#fca5a5")  # Couleur pour refusé

        # Ajout d'une barre de défilement verticale
        sb = ttk.Scrollbar(frm, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)  # Lie la scrollbar au tableau
        self.tree.pack(side="left", fill="both", expand=True)  # Place le tableau à gauche
        sb.pack(side="right", fill="y")  # Place la scrollbar à droite

        # Création des boutons d'action
        btn_row = tk.Frame(self.tab_req, bg=BG)
        btn_row.pack(pady=12)  # Frame pour les boutons
        tk.Button(btn_row, text="✅   Approuver", font=("Helvetica", 11, "bold"),
                  bg=SUCCESS, fg=BG, activebackground="#16a34a", relief="flat",
                  cursor="hand2", command=self._approve).pack(side="left", padx=12, ipadx=20, ipady=7)  # Bouton Approuver
        tk.Button(btn_row, text="❌   Refuser", font=("Helvetica", 11, "bold"),
                  bg=DANGER, fg=FG, activebackground="#dc2626", relief="flat",
                  cursor="hand2", command=self._reject).pack(side="left", padx=12, ipadx=20, ipady=7)  # Bouton Refuser

        self._refresh_req()  # Rafraîchit le tableau

    # Méthode pour rafraîchir le tableau des demandes
    def _refresh_req(self):
        for row in self.tree.get_children():  # Supprime toutes les lignes existantes
            self.tree.delete(row)
        vacs  = self.service.get_all_vacations()  # Récupère toutes les demandes
        users = {u["username"]: u.get("full_name", u["username"]) for u in self.service.load_users()}  # Dictionnaire des utilisateurs
        flt   = self.filter_var.get()  # Récupère le filtre actuel
        for v in reversed(vacs):  # Parcourt les demandes en ordre inverse (plus récentes en haut)
            if flt != "all" and v["status"] != flt:  # Applique le filtre
                continue
            name   = users.get(v["username"], v["username"])  # Nom complet ou identifiant
            days   = VacationService.count_days(v["start_date"], v["end_date"])  # Nombre de jours
            _, _, slabel = STATUS_CFG.get(v["status"], ("", "", v["status"]))  # Label du statut
            self.tree.insert("", "end", iid=str(v["id"]),  # Insère la ligne dans le tableau
                             values=(name, v["start_date"], v["end_date"],
                                     f"{days}j", v.get("reason", "—"),
                                     v.get("submitted_date", "—"), slabel),
                             tags=(v["status"],))  # Applique le tag pour la couleur

    # Méthode pour approuver une demande
    def _approve(self):
        sel = self.tree.selection()  # Récupère la sélection
        if not sel:
            messagebox.showwarning("Attention", "Sélectionnez une demande.", parent=self.root); return  # Avertissement si rien sélectionné
        self.service.update_status(int(sel[0]), "approved")  # Met à jour le statut
        messagebox.showinfo("Succès", "Congé approuvé ✅", parent=self.root)  # Message de succès
        self._refresh_req(); self._refresh_employees()  # Rafraîchit les vues

    # Méthode pour refuser une demande
    def _reject(self):
        sel = self.tree.selection()  # Récupère la sélection
        if not sel:
            messagebox.showwarning("Attention", "Sélectionnez une demande.", parent=self.root); return  # Avertissement si rien sélectionné
        self.service.update_status(int(sel[0]), "rejected")  # Met à jour le statut
        messagebox.showinfo("Info", "Congé refusé ❌", parent=self.root)  # Message d'info
        self._refresh_req(); self._refresh_employees()  # Rafraîchit les vues

    # ── Construction de l'onglet Calendrier ───────────────────────────────────
    def _build_calendar(self):
        self._render_calendar()  # Appelle la méthode de rendu

    # Méthode pour rendre le calendrier
    def _render_calendar(self):
        for w in self.tab_cal.winfo_children():  # Supprime tous les widgets existants
            w.destroy()

        # Création de la navigation (boutons précédent/suivant et titre du mois)
        nav = tk.Frame(self.tab_cal, bg=BG)
        nav.pack(pady=14)  # Frame pour la navigation
        tk.Button(nav, text="◀", command=self._prev_month,  # Bouton mois précédent
                  font=("Helvetica", 12), bg=ACCENT, fg=FG,
                  activebackground="#4f46e5", relief="flat", cursor="hand2",
                  width=3).pack(side="left", padx=6)
        _label(nav, f"{calendar.month_name[self.cal_month]}  {self.cal_year}",  # Titre du mois et année
               15, True, FG, BG, "center").pack(side="left", padx=30)
        tk.Button(nav, text="▶", command=self._next_month,  # Bouton mois suivant
                  font=("Helvetica", 12), bg=ACCENT, fg=FG,
                  activebackground="#4f46e5", relief="flat", cursor="hand2",
                  width=3).pack(side="left", padx=6)

        # Création de la grille du calendrier
        grid = tk.Frame(self.tab_cal, bg=BG)
        grid.pack(padx=24, pady=4, fill="both", expand=True)  # Frame pour la grille

        # En-têtes des jours de la semaine
        day_names = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        for i, d in enumerate(day_names):
            fg = DANGER if i >= 5 else MUTED  # Couleur rouge pour samedi/dimanche
            _label(grid, d, 10, True, fg, BG, "center").grid(row=0, column=i, padx=3, pady=4, sticky="ew")  # Label du jour
            grid.grid_columnconfigure(i, weight=1)  # Configuration des colonnes

        # Récupération des données pour le calendrier
        vacs     = self.service.get_all_vacations()  # Toutes les demandes
        users    = {u["username"]: u.get("full_name", u["username"]) for u in self.service.load_users()}  # Utilisateurs
        approved = [v for v in vacs if v["status"] == "approved"]  # Demandes approuvées
        today    = date.today()  # Date d'aujourd'hui

        # Parcours des semaines et jours du mois
        for week_i, week in enumerate(calendar.monthcalendar(self.cal_year, self.cal_month), 1):
            for day_i, day in enumerate(week):
                if day == 0:  # Jour vide (pas dans le mois)
                    tk.Label(grid, text="", bg=BG).grid(row=week_i, column=day_i, padx=3, pady=3, sticky="nsew")
                    continue

                cur = date(self.cal_year, self.cal_month, day)  # Date actuelle
                on_vac = []  # Liste des employés en congé ce jour
                for v in approved:
                    try:
                        if date.fromisoformat(v["start_date"]) <= cur <= date.fromisoformat(v["end_date"]):  # Vérifie si en congé
                            name = users.get(v["username"], v["username"])  # Nom de l'employé
                            on_vac.append(name.split()[0])  # Ajoute le prénom
                    except Exception:
                        pass  # Ignore les erreurs de parsing

                is_today   = cur == today  # Vérifie si c'est aujourd'hui
                is_weekend = day_i >= 5    # Vérifie si week-end

                # Détermine les couleurs selon le jour
                if is_today:
                    bg, num_fg = ACCENT, FG  # Aujourd'hui
                elif on_vac:
                    bg, num_fg = "#1e3a5f", "#93c5fd"  # En congé
                elif is_weekend:
                    bg, num_fg = "#0d1b2a", MUTED  # Week-end
                else:
                    bg, num_fg = PANEL, FG  # Jour normal

                # Création de la cellule du jour
                cell = tk.Frame(grid, bg=bg, bd=0, highlightthickness=1,
                                highlightbackground=BORDER)  # Frame pour la cellule
                cell.grid(row=week_i, column=day_i, padx=3, pady=3, sticky="nsew")
                grid.grid_rowconfigure(week_i, weight=1)  # Configuration des lignes

                _label(cell, str(day), 11, True, num_fg, bg).pack(anchor="nw", padx=5, pady=(4, 0))  # Numéro du jour
                if on_vac:  # Si des employés en congé
                    names = ", ".join(on_vac[:2])  # Affiche jusqu'à 2 noms
                    if len(on_vac) > 2:
                        names += f" +{len(on_vac)-2}"  # Ajoute le nombre supplémentaire
                    _label(cell, names, 8, False, "#93c5fd", bg).pack(anchor="w", padx=5)  # Label des noms

        # Création de la légende
        leg = tk.Frame(self.tab_cal, bg=BG)
        leg.pack(pady=10)  # Frame pour la légende
        for color, txt in [(ACCENT, "Aujourd'hui"), ("#1e3a5f", "En congé"), (PANEL, "Disponible")]:  # Éléments de légende
            tk.Frame(leg, bg=color, width=18, height=14, bd=1,
                     highlightthickness=1, highlightbackground=BORDER).pack(side="left", padx=4)  # Carré coloré
            _label(leg, txt, 9, False, MUTED, BG).pack(side="left", padx=(2, 14))  # Texte de légende

    # Méthode pour aller au mois précédent
    def _prev_month(self):
        self.cal_month -= 1  # Décrémente le mois
        if self.cal_month < 1: self.cal_month = 12; self.cal_year -= 1  # Si janvier, passe à décembre de l'année précédente
        self._render_calendar()  # Rend le calendrier

    # Méthode pour aller au mois suivant
    def _next_month(self):
        self.cal_month += 1  # Incrémente le mois
        if self.cal_month > 12: self.cal_month = 1; self.cal_year += 1  # Si décembre, passe à janvier de l'année suivante
        self._render_calendar()  # Rend le calendrier

    # ── Construction de l'onglet Employés ─────────────────────────────────────
    def _build_employees(self):
        self.emp_scroll_frame = tk.Frame(self.tab_emp, bg=BG)  # Frame pour le contenu défilable
        self.emp_scroll_frame.pack(fill="both", expand=True, padx=24, pady=16)
        self._refresh_employees()  # Rafraîchit la vue des employés

    # Méthode pour rafraîchir la vue des employés
    def _refresh_employees(self):
        for w in self.emp_scroll_frame.winfo_children():  # Supprime tous les widgets existants
            w.destroy()

        _label(self.emp_scroll_frame, "Vue d'ensemble des employees",  # Titre de la section
               14, True, FG, BG).pack(anchor="w", pady=(0, 12))

        users = [u for u in self.service.load_users() if u["role"] == "employee"]  # Liste des employés
        for u in users:  # Parcourt chaque employé
            total     = u.get("total_days", 25)  # Jours de congé totaux (défaut 25)
            used      = self.service.get_used_days(u["username"])  # Jours utilisés
            remaining = total - used  # Jours restants
            pct       = max(0.0, min(1.0, used / total)) if total else 0  # Pourcentage utilisé

            # Couleur de la barre selon le pourcentage
            bar_color = SUCCESS if pct < 0.6 else WARNING if pct < 0.85 else DANGER

            # Création de la carte pour l'employé
            card = tk.Frame(self.emp_scroll_frame, bg=PANEL, bd=0,
                            highlightthickness=1, highlightbackground=BORDER)  # Frame de la carte
            card.pack(fill="x", pady=6, ipady=6)  # Étend horizontalement

            # Partie supérieure de la carte
            top = tk.Frame(card, bg=PANEL)
            top.pack(fill="x", padx=16, pady=(10, 4))  # Frame supérieur
            _label(top, u.get("full_name", u["username"]), 13, True, FG, PANEL).pack(side="left")  # Nom de l'employé
            _label(top, f"{remaining} / {total} jours restants", 10, False,
                   bar_color, PANEL).pack(side="right")  # Jours restants

            # Barre de progression pour les jours utilisés
            bar_bg = tk.Frame(card, bg=BORDER, height=8)  # Fond de la barre
            bar_bg.pack(fill="x", padx=16, pady=(2, 6))
            bar_bg.update_idletasks()  # Met à jour pour obtenir les dimensions
            bar_fill = tk.Frame(bar_bg, bg=bar_color, height=8)  # Partie remplie
            bar_fill.place(relwidth=pct, relheight=1)  # Place selon le pourcentage

            # Résumé des demandes
            my_vacs = self.service.get_user_vacations(u["username"])  # Demandes de l'employé
            pending  = len([v for v in my_vacs if v["status"] == "pending"])   # En attente
            approved = len([v for v in my_vacs if v["status"] == "approved"])  # Approuvées
            rejected = len([v for v in my_vacs if v["status"] == "rejected"])  # Refusées
            _label(card,  # Label avec le résumé
                   f"  ⏳ {pending} en attente   ✅ {approved} approuvés   ❌ {rejected} refusés   |   {used} jours consommés",
                   9, False, MUTED, PANEL).pack(anchor="w", padx=16, pady=(0, 6))
