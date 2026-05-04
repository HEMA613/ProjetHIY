import calendar
import os
import sys
import tkinter as tk
from datetime import date
from tkinter import messagebox
from tkinter import ttk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
services_dir = os.path.join(BASE_DIR, "frontend", "services")
sys.path.insert(0, services_dir)

from vacation_service import VacationService
from dashboard_common import (
    ACCENT,
    BG,
    BORDER,
    DANGER,
    ENTRY,
    FG,
    MUTED,
    PANEL,
    SUCCESS,
    WARNING,
    STATUS_CFG,
    _label,
    setup_notebook_style,
)


# Classe principale pour le tableau de bord de l'employé
class EmployeeDashboard:
    # Initialisation de la classe
    def __init__(self, root, user, on_logout=None):
        self.root = root  # Fenêtre principale Tkinter
        self.user = user  # Informations de l'utilisateur connecté
        self.on_logout = on_logout  # Callback pour la déconnexion
        self.service = VacationService()  # Instance du service de congés
        self.cal_year = date.today().year  # Année actuelle pour le calendrier
        self.cal_month = date.today().month  # Mois actuel pour le calendrier

        # Configuration de la fenêtre
        self.root.title(f"Mon Espace — {user['full_name']}")  # Titre de la fenêtre
        self.root.geometry("920x660")  # Taille de la fenêtre
        self.root.configure(bg=BG)  # Couleur de fond
        self.root.resizable(True, True)  # Permet le redimensionnement
        self._center()  # Centre la fenêtre sur l'écran
        self._build()  # Construit l'interface

    # Méthode pour centrer la fenêtre sur l'écran
    def _center(self):
        self.root.update_idletasks()  # Met à jour les tâches de la fenêtre
        x = (self.root.winfo_screenwidth() - 920) // 2  # Position x centrée
        y = (self.root.winfo_screenheight() - 660) // 2  # Position y centrée
        self.root.geometry(f"920x660+{x}+{y}")  # Applique la géométrie

    def _logout(self):
        self.root.destroy()
        if callable(self.on_logout):
            self.on_logout()

    # ── Construction de la structure de l'interface ──────────────────────────
    def _build(self):
        # Création de l'en-tête
        hdr = tk.Frame(self.root, bg=ACCENT, height=54)
        hdr.pack(fill="x")  # Étend horizontalement
        hdr.pack_propagate(False)  # Empêche le redimensionnement automatique
        _label(
            hdr, "✦  Gestion des Congés  ·  Espace Employee", 13, True, FG, ACCENT
        ).pack(
            side="left", padx=22, pady=14
        )  # Titre à gauche
        _label(hdr, f"👤  {self.user['full_name']}", 10, False, "#c7d2fe", ACCENT).pack(
            side="right", padx=22
        )  # Nom de l'utilisateur à droite
        tk.Button(
            hdr,
            text="Déconnexion",
            font=("Helvetica", 10, "bold"),
            bg=DANGER,
            fg=FG,
            activebackground="#dc2626",
            relief="flat",
            cursor="hand2",
            command=self._logout,
        ).pack(side="right", padx=12, pady=10)

        # Configuration du style du notebook (onglets)
        setup_notebook_style()

        # Création du notebook avec les onglets
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True)  # Étend dans toute la fenêtre

        # Création des onglets
        self.tab_home = tk.Frame(nb, bg=BG)
        nb.add(self.tab_home, text="  🏠  Tableau de bord  ")  # Onglet Accueil
        self.tab_req = tk.Frame(nb, bg=BG)
        nb.add(self.tab_req, text="  ➕  Nouvelle demande  ")  # Onglet Nouvelle demande
        self.tab_cal = tk.Frame(nb, bg=BG)
        nb.add(self.tab_cal, text="  📅  Calendrier  ")  # Onglet Calendrier

        # Construction des contenus des onglets
        self._build_home()  # Construit l'onglet Accueil
        self._build_request_form()  # Construit l'onglet Nouvelle demande
        self._build_calendar()  # Construit l'onglet Calendrier

    # ── Construction de l'onglet Accueil ─────────────────────────────────────────
    def _build_home(self):
        for w in self.tab_home.winfo_children():  # Supprime tous les widgets existants
            w.destroy()

        # Récupération des données de l'utilisateur
        total = self.user.get("total_days", 25)  # Jours de congé totaux
        used = self.service.get_used_days(self.user["username"])  # Jours utilisés
        remaining = total - used  # Jours restants
        my_vacs = self.service.get_user_vacations(
            self.user["username"]
        )  # Demandes de l'utilisateur
        pending = len(
            [v for v in my_vacs if v["status"] == "pending"]
        )  # Nombre en attente
        approved = len(
            [v for v in my_vacs if v["status"] == "approved"]
        )  # Nombre approuvées

        # Titre et sous-titre
        _label(
            self.tab_home,
            f"Bonjour, {self.user['full_name']} 👋",
            16,
            True,
            FG,
            BG,
        ).pack(anchor="w", padx=24, pady=(16, 4))
        _label(
            self.tab_home,
            "Voici un résumé de vos congés.",
            10,
            False,
            MUTED,
            BG,
        ).pack(anchor="w", padx=24, pady=(0, 10))

        # Ligne de cartes de statistiques
        cards_row = tk.Frame(self.tab_home, bg=BG)
        cards_row.pack(fill="x", padx=20, pady=4)

        # Création des cartes pour chaque statistique
        for count, label, color, emoji in [
            (remaining, "Jours restants", ACCENT, "📆"),  # Jours restants
            (used, "Jours utilisés", DANGER, "📤"),  # Jours utilisés
            (pending, "En attente", WARNING, "⏳"),  # En attente
            (approved, "Approuvés", SUCCESS, "✅"),  # Approuvées
        ]:
            c = tk.Frame(cards_row, bg=PANEL)  # Frame pour la carte
            c.pack(side="left", padx=6, ipadx=24, ipady=10, expand=True, fill="x")
            _label(c, emoji, 18, False, color, PANEL, "center").pack()  # Emoji
            _label(c, str(count), 24, True, color, PANEL, "center").pack()  # Nombre
            _label(c, label, 9, False, MUTED, PANEL, "center").pack(
                pady=(0, 4)
            )  # Label

        # Barre de progression pour l'utilisation des jours
        pct = max(0.0, min(1.0, used / total)) if total else 0  # Pourcentage utilisé
        bar_color = (
            SUCCESS if pct < 0.6 else WARNING if pct < 0.85 else DANGER
        )  # Couleur selon le pourcentage

        prog_card = tk.Frame(
            self.tab_home, bg=PANEL
        )  # Carte pour la barre de progression
        prog_card.pack(fill="x", padx=26, pady=10, ipady=8)
        top_row = tk.Frame(prog_card, bg=PANEL)
        top_row.pack(fill="x", padx=16, pady=(10, 4))
        _label(
            top_row,
            "Utilisation des jours de congé",
            11,
            True,
            FG,
            PANEL,
        ).pack(side="left")  # Titre
        _label(
            top_row,
            f"{used} / {total} jours",
            10,
            False,
            bar_color,
            PANEL,
        ).pack(side="right")  # Valeur
        bar_bg = tk.Frame(prog_card, bg=BORDER, height=10)  # Fond de la barre
        bar_bg.pack(fill="x", padx=16, pady=(0, 10))
        bar_fill = tk.Frame(bar_bg, bg=bar_color, height=10)  # Partie remplie
        bar_fill.place(relwidth=pct, relheight=1)  # Place selon le pourcentage

        # Liste des demandes
        _label(self.tab_home, "Mes demandes", 13, True, FG, BG).pack(
            anchor="w", padx=24, pady=(8, 4)
        )  # Titre de la section

        list_frame = tk.Frame(self.tab_home, bg=BG)  # Frame pour la liste
        list_frame.pack(fill="both", expand=True, padx=20)

        if not my_vacs:  # Si aucune demande
            _label(
                list_frame,
                "Aucune demande pour l'instant. Utilisez l'onglet ➕ pour en créer une.",
                10,
                False,
                MUTED,
                BG,
                "center",
            ).pack(pady=30)
        else:  # Sinon, affiche chaque demande
            for v in reversed(
                my_vacs
            ):  # Parcourt en ordre inverse (plus récentes en haut)
                self._req_card(list_frame, v)  # Crée une carte pour chaque demande

    # Méthode pour créer une carte de demande
    def _req_card(self, parent, v):
        bg, fg, slabel = STATUS_CFG.get(
            v["status"], (PANEL, MUTED, v["status"])
        )  # Couleurs selon le statut
        try:
            s = date.fromisoformat(v["start_date"])  # Date de début
            e = date.fromisoformat(v["end_date"])  # Date de fin
            days = (e - s).days + 1  # Nombre de jours
            # Formaté avec ←
            suffix = "s" if days > 1 else ""
            period = (
                f"{s.strftime('%d %b')} → "
                f"{e.strftime('%d %b %Y')}   ({days} jour{suffix})"
            )
        except Exception:
            period = f"{v['start_date']} → {v['end_date']}"  # Format de secours

        card = tk.Frame(
            parent, bg=bg, highlightthickness=1, highlightbackground=BORDER
        )  # Frame de la carte
        card.pack(fill="x", pady=3)

        left = tk.Frame(card, bg=bg)  # Partie gauche
        left.pack(side="left", fill="both", expand=True, padx=12, pady=8)
        _label(left, period, 11, True, fg, bg).pack(anchor="w")  # Période
        if v.get("reason"):  # Si motif présent
            _label(left, v["reason"], 9, False, MUTED, bg).pack(anchor="w")  # Motif

        _label(card, slabel, 10, True, fg, bg).pack(
            side="right", padx=16
        )  # Statut à droite

    # ── Construction de l'onglet Nouvelle demande ──────────────────────────────
    def _build_request_form(self):
        outer = tk.Frame(self.tab_req, bg=BG)  # Frame externe centré
        outer.place(relx=0.5, rely=0.46, anchor="center", width=520, height=420)

        # Titre et sous-titre
        _label(outer, "📝  Nouvelle demande de congé", 15, True, FG, BG, "center").pack(
            pady=(10, 4)
        )
        _label(
            outer,
            "Remplissez les informations ci-dessous pour soumettre votre demande.",
            9,
            False,
            MUTED,
            BG,
            "center",
        ).pack(pady=(0, 18))

        form = tk.Frame(
            outer, bg=PANEL, highlightthickness=1, highlightbackground=BORDER
        )  # Frame du formulaire
        form.pack(fill="x")

        # Champ date de début
        self._form_field(form, "Date de début  (AAAA-MM-JJ)")  # Label
        self.start_e = self._form_entry(form)  # Champ de saisie

        # Champ date de fin
        self._form_field(form, "Date de fin  (AAAA-MM-JJ)")  # Label
        self.end_e = self._form_entry(form)  # Champ de saisie

        # Champ motif
        self._form_field(form, "Motif  (optionnel)")  # Label
        self.reason_e = self._form_entry(form)  # Champ de saisie

        # Information sur les jours restants
        total = self.user.get("total_days", 25)  # Jours totaux
        remaining = self.service.get_remaining_days(
            self.user["username"], total
        )  # Jours restants
        _label(
            form,
            f"ℹ️   Il vous reste {remaining} jour(s) de congé disponibles.",
            9,
            False,
            MUTED,
            PANEL,
        ).pack(anchor="w", padx=22, pady=(6, 14))

        # Bouton d'envoi
        tk.Button(
            form,
            text="Envoyer la demande  →",
            font=("Helvetica", 11, "bold"),
            bg=ACCENT,
            fg=FG,
            activebackground="#4f46e5",
            relief="flat",
            cursor="hand2",
            command=self._submit,
        ).pack(
            padx=22, fill="x", ipady=9, pady=(0, 22)
        )  # Bouton

    # Méthode helper pour créer un label de champ de formulaire
    def _form_field(self, parent, text):
        _label(parent, text, 10, False, MUTED, PANEL).pack(
            anchor="w", padx=22, pady=(16, 2)
        )

    # Méthode helper pour créer un champ de saisie de formulaire
    def _form_entry(self, parent):
        e = tk.Entry(
            parent,
            font=("Helvetica", 12),
            bg=ENTRY,
            fg=FG,
            insertbackground=FG,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )  # Champ avec style
        e.pack(padx=22, fill="x", ipady=7)
        return e

    # Méthode pour soumettre la demande
    def _submit(self):
        print("Soumission de la demande...")  # Log de soumission
        start = self.start_e.get().strip()  # Récupère la date de début
        end = self.end_e.get().strip()  # Récupère la date de fin
        reason = self.reason_e.get().strip()  # Récupère le motif

        if not start or not end:  # Vérifie que les dates sont remplies
            messagebox.showwarning(
                "Attention", "Les dates sont obligatoires.", parent=self.root
            )
            return
        try:
            s = date.fromisoformat(start)  # Parse la date de début
            e = date.fromisoformat(end)  # Parse la date de fin
        except ValueError:  # Si format invalide
            messagebox.showerror(
                "Erreur", "Format invalide. Utilisez AAAA-MM-JJ.", parent=self.root
            )
            return
        if e < s:  # Vérifie que la fin est après le début
            messagebox.showerror(
                "Erreur",
                "La date de fin doit être après la date de début.",
                parent=self.root,
            )
            return

        days = (e - s).days + 1  # Calcule le nombre de jours
        total = self.user.get("total_days", 25)  # Jours totaux
        remaining = self.service.get_remaining_days(
            self.user["username"], total
        )  # Jours restants
        if days > remaining:  # Vérifie qu'il y a assez de jours
            messagebox.showerror(
                "Erreur",
                f"Vous demandez {days} jours mais il vous en reste {remaining}.",
                parent=self.root,
            )
            return

        # Soumet la demande
        self.service.submit_request(self.user["username"], start, end, reason)
        messagebox.showinfo(
            "Succès ✅",
            (
                f"Demande de {days} jour(s) envoyée avec succès !\n"
                "Elle est en attente de validation."
            ),
            parent=self.root,
        )

        # Vide les champs et rafraîchit l'accueil
        self.start_e.delete(0, tk.END)
        self.end_e.delete(0, tk.END)
        self.reason_e.delete(0, tk.END)
        self._build_home()

    # ── Construction de l'onglet Calendrier ───────────────────────────────────
    def _build_calendar(self):
        self._render_calendar()  # Appelle la méthode de rendu

    # Méthode pour rendre le calendrier
    def _render_calendar(self):
        for w in self.tab_cal.winfo_children():  # Supprime tous les widgets existants
            w.destroy()

        # Création de la navigation
        nav = tk.Frame(self.tab_cal, bg=BG)
        nav.pack(pady=14)
        tk.Button(
            nav,
            text="◀",
            command=self._prev_month,  # Bouton mois précédent
            font=("Helvetica", 12),
            bg=ACCENT,
            fg=FG,
            activebackground="#4f46e5",
            relief="flat",
            cursor="hand2",
            width=3,
        ).pack(side="left", padx=6)
        _label(
            nav,
            f"{calendar.month_name[self.cal_month]}  {self.cal_year}",  # Titre du mois
            15,
            True,
            FG,
            BG,
            "center",
        ).pack(side="left", padx=30)
        tk.Button(
            nav,
            text="▶",
            command=self._next_month,  # Bouton mois suivant
            font=("Helvetica", 12),
            bg=ACCENT,
            fg=FG,
            activebackground="#4f46e5",
            relief="flat",
            cursor="hand2",
            width=3,
        ).pack(side="left", padx=6)

        # Création de la grille du calendrier
        grid = tk.Frame(self.tab_cal, bg=BG)
        grid.pack(padx=24, pady=4, fill="both", expand=True)

        # En-têtes des jours
        for i, d in enumerate(["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]):
            fg = DANGER if i >= 5 else MUTED  # Couleur rouge pour week-end
            _label(grid, d, 10, True, fg, BG, "center").grid(
                row=0, column=i, padx=3, pady=4, sticky="ew"
            )
            grid.grid_columnconfigure(i, weight=1)

        # Récupération des données
        my_vacs = self.service.get_user_vacations(
            self.user["username"]
        )  # Demandes de l'utilisateur
        approved = [v for v in my_vacs if v["status"] == "approved"]  # Approuvées
        pending = [v for v in my_vacs if v["status"] == "pending"]  # En attente
        today = date.today()  # Aujourd'hui

        # Parcours des semaines et jours
        for week_i, week in enumerate(
            calendar.monthcalendar(self.cal_year, self.cal_month), 1
        ):
            for day_i, day in enumerate(week):
                if day == 0:  # Jour vide
                    tk.Label(grid, text="", bg=BG).grid(
                        row=week_i, column=day_i, padx=3, pady=3, sticky="nsew"
                    )
                    continue

                cur = date(self.cal_year, self.cal_month, day)  # Date actuelle
                # Vérifie si le jour est dans une période approuvée
                is_app = any(
                    date.fromisoformat(v["start_date"])
                    <= cur
                    <= date.fromisoformat(v["end_date"])
                    for v in approved
                )
                # Vérifie si le jour est dans une période en attente
                is_pen = any(
                    date.fromisoformat(v["start_date"])
                    <= cur
                    <= date.fromisoformat(v["end_date"])
                    for v in pending
                )
                is_today = cur == today  # Aujourd'hui
                is_weekend = day_i >= 5  # Week-end

                # Détermine les couleurs et marqueurs
                if is_today:
                    bg, num_fg, marker = ACCENT, FG, ""  # Aujourd'hui
                elif is_app:
                    bg, num_fg, marker = "#14532d", "#86efac", "✅"  # Approuvé
                elif is_pen:
                    bg, num_fg, marker = "#431407", "#fdba74", "⏳"  # En attente
                elif is_weekend:
                    bg, num_fg, marker = "#0d1b2a", MUTED, ""  # Week-end
                else:
                    bg, num_fg, marker = PANEL, FG, ""  # Normal

                # Création de la cellule
                cell = tk.Frame(
                    grid, bg=bg, highlightthickness=1, highlightbackground=BORDER
                )
                cell.grid(row=week_i, column=day_i, padx=3, pady=3, sticky="nsew")
                grid.grid_rowconfigure(week_i, weight=1)

                _label(cell, str(day), 11, True, num_fg, bg).pack(
                    anchor="nw", padx=5, pady=(4, 0)
                )  # Numéro du jour
                if marker:  # Si marqueur présent
                    _label(
                        cell, marker, 10, False, num_fg, bg, "center"
                    ).pack()  # Marqueur

        # Création de la légende
        leg = tk.Frame(self.tab_cal, bg=BG)
        leg.pack(pady=8)
        for color, txt in [
            (ACCENT, "Aujourd'hui"),  # Aujourd'hui
            ("#14532d", "Congé approuvé"),  # Approuvé
            ("#431407", "En attente"),  # En attente
            (PANEL, "Disponible"),  # Disponible
        ]:
            tk.Frame(
                leg,
                bg=color,
                width=18,
                height=14,
                highlightthickness=1,
                highlightbackground=BORDER,
            ).pack(
                side="left", padx=4
            )  # Carré coloré
            _label(leg, txt, 9, False, MUTED, BG).pack(
                side="left", padx=(2, 16)
            )  # Texte

    # Méthode pour aller au mois précédent
    def _prev_month(self):
        self.cal_month -= 1  # Décrémente le mois
        if self.cal_month < 1:
            self.cal_month = 12
            self.cal_year -= 1  # Si janvier, passe à décembre de l'année précédente
        self._render_calendar()  # Rend le calendrier

    # Méthode pour aller au mois suivant
    def _next_month(self):
        self.cal_month += 1  # Incrémente le mois
        if self.cal_month > 12:
            self.cal_month = 1
            self.cal_year += 1  # Si décembre, passe à janvier de l'année suivante
        self._render_calendar()  # Rend le calendrier
