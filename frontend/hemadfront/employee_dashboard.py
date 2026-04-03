import tkinter as tk
from tkinter import ttk, messagebox
import calendar, sys, os
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
services_dir = os.path.join(BASE_DIR, "hemadfront", "services")
sys.path.insert(0, services_dir)
from vacation_service import VacationService

# ── palette ────────────────────────────────────────────────────
BG      = "#0f172a"
PANEL   = "#1e293b"
CARD    = "#263348"
ACCENT  = "#6366f1"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"
DANGER  = "#ef4444"
FG      = "#f8fafc"
MUTED   = "#94a3b8"
BORDER  = "#334155"
ENTRY   = "#0f172a"

STATUS_CFG = {
    "pending":  ("#451a03", "#f59e0b", "⏳ En attente"),
    "approved": ("#052e16", "#22c55e", "✅ Approuvé"),
    "rejected": ("#450a0a", "#ef4444", "❌ Refusé"),
}


def _label(parent, text, size=10, bold=False, fg=FG, bg=None, anchor="w"):
    bg = bg or parent.cget("bg")
    w  = "bold" if bold else "normal"
    return tk.Label(parent, text=text, font=("Helvetica", size, w),
                    fg=fg, bg=bg, anchor=anchor)


class EmployeeDashboard:
    def __init__(self, root, user):
        self.root    = root
        self.user    = user
        self.service = VacationService()
        self.cal_year  = date.today().year
        self.cal_month = date.today().month

        self.root.title(f"Mon Espace — {user['full_name']}")
        self.root.geometry("920x660")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self._center()
        self._build()

    def _center(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 920) // 2
        y = (self.root.winfo_screenheight() - 660) // 2
        self.root.geometry(f"920x660+{x}+{y}")

    # ── skeleton ──────────────────────────────────────────────
    def _build(self):
        hdr = tk.Frame(self.root, bg=ACCENT, height=54)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        _label(hdr, "✦  Gestion des Congés  ·  Espace Employee", 13, True, FG, ACCENT).pack(side="left", padx=22, pady=14)
        _label(hdr, f"👤  {self.user['full_name']}", 10, False, "#c7d2fe", ACCENT).pack(side="right", padx=22)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook",       background=BG,    borderwidth=0)
        style.configure("TNotebook.Tab",   background=PANEL, foreground=MUTED,
                        font=("Helvetica", 10), padding=[18, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", CARD)],
                  foreground=[("selected", FG)])

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True)

        self.tab_home = tk.Frame(nb, bg=BG); nb.add(self.tab_home, text="  🏠  Tableau de bord  ")
        self.tab_req  = tk.Frame(nb, bg=BG); nb.add(self.tab_req,  text="  ➕  Nouvelle demande  ")
        self.tab_cal  = tk.Frame(nb, bg=BG); nb.add(self.tab_cal,  text="  📅  Calendrier  ")

        self._build_home()
        self._build_request_form()
        self._build_calendar()

    # ── TAB 1 : Home ─────────────────────────────────────────
    def _build_home(self):
        for w in self.tab_home.winfo_children():
            w.destroy()

        total     = self.user.get("total_days", 25)
        used      = self.service.get_used_days(self.user["username"])
        remaining = total - used
        my_vacs   = self.service.get_user_vacations(self.user["username"])
        pending   = len([v for v in my_vacs if v["status"] == "pending"])
        approved  = len([v for v in my_vacs if v["status"] == "approved"])

        _label(self.tab_home, f"Bonjour, {self.user['full_name']} 👋",
               16, True, FG, BG).pack(anchor="w", padx=24, pady=(16, 4))
        _label(self.tab_home, "Voici un résumé de vos congés.",
               10, False, MUTED, BG).pack(anchor="w", padx=24, pady=(0, 10))

        # Stats cards
        cards_row = tk.Frame(self.tab_home, bg=BG)
        cards_row.pack(fill="x", padx=20, pady=4)

        for count, label, color, emoji in [
            (remaining, "Jours restants", ACCENT,   "📆"),
            (used,      "Jours utilisés", DANGER,   "📤"),
            (pending,   "En attente",     WARNING,  "⏳"),
            (approved,  "Approuvés",      SUCCESS,  "✅"),
        ]:
            c = tk.Frame(cards_row, bg=PANEL)
            c.pack(side="left", padx=6, ipadx=24, ipady=10, expand=True, fill="x")
            _label(c, emoji,       18, False, color,  PANEL, "center").pack()
            _label(c, str(count),  24, True,  color,  PANEL, "center").pack()
            _label(c, label,        9, False, MUTED,  PANEL, "center").pack(pady=(0, 4))

        # Progress bar
        pct       = max(0.0, min(1.0, used / total)) if total else 0
        bar_color = SUCCESS if pct < 0.6 else WARNING if pct < 0.85 else DANGER

        prog_card = tk.Frame(self.tab_home, bg=PANEL)
        prog_card.pack(fill="x", padx=26, pady=10, ipady=8)
        top_row = tk.Frame(prog_card, bg=PANEL)
        top_row.pack(fill="x", padx=16, pady=(10, 4))
        _label(top_row, f"Utilisation des jours de congé", 11, True, FG, PANEL).pack(side="left")
        _label(top_row, f"{used} / {total} jours", 10, False, bar_color, PANEL).pack(side="right")
        bar_bg = tk.Frame(prog_card, bg=BORDER, height=10)
        bar_bg.pack(fill="x", padx=16, pady=(0, 10))
        bar_fill = tk.Frame(bar_bg, bg=bar_color, height=10)
        bar_fill.place(relwidth=pct, relheight=1)

        # Requests list
        _label(self.tab_home, "Mes demandes", 13, True, FG, BG).pack(anchor="w", padx=24, pady=(8, 4))

        list_frame = tk.Frame(self.tab_home, bg=BG)
        list_frame.pack(fill="both", expand=True, padx=20)

        if not my_vacs:
            _label(list_frame, "Aucune demande pour l'instant. Utilisez l'onglet ➕ pour en créer une.",
                   10, False, MUTED, BG, "center").pack(pady=30)
        else:
            for v in reversed(my_vacs):
                self._req_card(list_frame, v)

    def _req_card(self, parent, v):
        bg, fg, slabel = STATUS_CFG.get(v["status"], (PANEL, MUTED, v["status"]))
        try:
            s = date.fromisoformat(v["start_date"])
            e = date.fromisoformat(v["end_date"])
            days    = (e - s).days + 1
            period  = f"{s.strftime('%d %b')} → {e.strftime('%d %b %Y')}   ({days} jour{'s' if days > 1 else ''})"
        except Exception:
            period = f"{v['start_date']} → {v['end_date']}"

        card = tk.Frame(parent, bg=bg, highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="x", pady=3)

        left = tk.Frame(card, bg=bg)
        left.pack(side="left", fill="both", expand=True, padx=12, pady=8)
        _label(left, period, 11, True, fg, bg).pack(anchor="w")
        if v.get("reason"):
            _label(left, v["reason"], 9, False, MUTED, bg).pack(anchor="w")

        _label(card, slabel, 10, True, fg, bg).pack(side="right", padx=16)

    # ── TAB 2 : Nouvelle demande ──────────────────────────────
    def _build_request_form(self):
        outer = tk.Frame(self.tab_req, bg=BG)
        outer.place(relx=0.5, rely=0.46, anchor="center", width=520, height=420)

        _label(outer, "📝  Nouvelle demande de congé", 15, True, FG, BG, "center").pack(pady=(10, 4))
        _label(outer, "Remplissez les informations ci-dessous pour soumettre votre demande.",
               9, False, MUTED, BG, "center").pack(pady=(0, 18))

        form = tk.Frame(outer, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
        form.pack(fill="x")

        self._form_field(form, "Date de début  (AAAA-MM-JJ)")
        self.start_e = self._form_entry(form)

        self._form_field(form, "Date de fin  (AAAA-MM-JJ)")
        self.end_e = self._form_entry(form)

        self._form_field(form, "Motif  (optionnel)")
        self.reason_e = self._form_entry(form)

        # Days remaining info
        total     = self.user.get("total_days", 25)
        remaining = self.service.get_remaining_days(self.user["username"], total)
        _label(form, f"ℹ️   Il vous reste {remaining} jour(s) de congé disponibles.",
               9, False, MUTED, PANEL).pack(anchor="w", padx=22, pady=(6, 14))

        tk.Button(form, text="Envoyer la demande  →",
                  font=("Helvetica", 11, "bold"),
                  bg=ACCENT, fg=FG,
                  activebackground="#4f46e5", relief="flat",
                  cursor="hand2", command=self._submit).pack(padx=22, fill="x", ipady=9, pady=(0, 22))

    def _form_field(self, parent, text):
        _label(parent, text, 10, False, MUTED, PANEL).pack(anchor="w", padx=22, pady=(16, 2))

    def _form_entry(self, parent):
        e = tk.Entry(parent, font=("Helvetica", 12),
                     bg=ENTRY, fg=FG, insertbackground=FG,
                     relief="flat", bd=0,
                     highlightthickness=1, highlightbackground=BORDER,
                     highlightcolor=ACCENT)
        e.pack(padx=22, fill="x", ipady=7)
        return e

    def _submit(self):
        start  = self.start_e.get().strip()
        end    = self.end_e.get().strip()
        reason = self.reason_e.get().strip()

        if not start or not end:
            messagebox.showwarning("Attention", "Les dates sont obligatoires.", parent=self.root)
            return
        try:
            s = date.fromisoformat(start)
            e = date.fromisoformat(end)
        except ValueError:
            messagebox.showerror("Erreur", "Format invalide. Utilisez AAAA-MM-JJ.", parent=self.root)
            return
        if e < s:
            messagebox.showerror("Erreur", "La date de fin doit être après la date de début.", parent=self.root)
            return

        days      = (e - s).days + 1
        total     = self.user.get("total_days", 25)
        remaining = self.service.get_remaining_days(self.user["username"], total)
        if days > remaining:
            messagebox.showerror("Erreur", f"Vous demandez {days} jours mais il vous en reste {remaining}.", parent=self.root)
            return

        self.service.submit_request(self.user["username"], start, end, reason)
        messagebox.showinfo("Succès ✅", f"Demande de {days} jour(s) envoyée avec succès !\nElle est en attente de validation.", parent=self.root)

        self.start_e.delete(0, tk.END)
        self.end_e.delete(0, tk.END)
        self.reason_e.delete(0, tk.END)
        self._build_home()

    # ── TAB 3 : Calendrier ───────────────────────────────────
    def _build_calendar(self):
        self._render_calendar()

    def _render_calendar(self):
        for w in self.tab_cal.winfo_children():
            w.destroy()

        nav = tk.Frame(self.tab_cal, bg=BG)
        nav.pack(pady=14)
        tk.Button(nav, text="◀", command=self._prev_month,
                  font=("Helvetica", 12), bg=ACCENT, fg=FG,
                  activebackground="#4f46e5", relief="flat", cursor="hand2",
                  width=3).pack(side="left", padx=6)
        _label(nav, f"{calendar.month_name[self.cal_month]}  {self.cal_year}",
               15, True, FG, BG, "center").pack(side="left", padx=30)
        tk.Button(nav, text="▶", command=self._next_month,
                  font=("Helvetica", 12), bg=ACCENT, fg=FG,
                  activebackground="#4f46e5", relief="flat", cursor="hand2",
                  width=3).pack(side="left", padx=6)

        grid = tk.Frame(self.tab_cal, bg=BG)
        grid.pack(padx=24, pady=4, fill="both", expand=True)

        for i, d in enumerate(["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]):
            fg = DANGER if i >= 5 else MUTED
            _label(grid, d, 10, True, fg, BG, "center").grid(row=0, column=i, padx=3, pady=4, sticky="ew")
            grid.grid_columnconfigure(i, weight=1)

        my_vacs  = self.service.get_user_vacations(self.user["username"])
        approved = [v for v in my_vacs if v["status"] == "approved"]
        pending  = [v for v in my_vacs if v["status"] == "pending"]
        today    = date.today()

        for week_i, week in enumerate(calendar.monthcalendar(self.cal_year, self.cal_month), 1):
            for day_i, day in enumerate(week):
                if day == 0:
                    tk.Label(grid, text="", bg=BG).grid(row=week_i, column=day_i, padx=3, pady=3, sticky="nsew")
                    continue

                cur = date(self.cal_year, self.cal_month, day)
                is_app = any(
                    date.fromisoformat(v["start_date"]) <= cur <= date.fromisoformat(v["end_date"])
                    for v in approved
                )
                is_pen = any(
                    date.fromisoformat(v["start_date"]) <= cur <= date.fromisoformat(v["end_date"])
                    for v in pending
                )
                is_today   = cur == today
                is_weekend = day_i >= 5

                if is_today:
                    bg, num_fg, marker = ACCENT, FG, ""
                elif is_app:
                    bg, num_fg, marker = "#14532d", "#86efac", "✅"
                elif is_pen:
                    bg, num_fg, marker = "#431407", "#fdba74", "⏳"
                elif is_weekend:
                    bg, num_fg, marker = "#0d1b2a", MUTED, ""
                else:
                    bg, num_fg, marker = PANEL, FG, ""

                cell = tk.Frame(grid, bg=bg, highlightthickness=1, highlightbackground=BORDER)
                cell.grid(row=week_i, column=day_i, padx=3, pady=3, sticky="nsew")
                grid.grid_rowconfigure(week_i, weight=1)

                _label(cell, str(day), 11, True, num_fg, bg).pack(anchor="nw", padx=5, pady=(4, 0))
                if marker:
                    _label(cell, marker, 10, False, num_fg, bg, "center").pack()

        # Legend
        leg = tk.Frame(self.tab_cal, bg=BG)
        leg.pack(pady=8)
        for color, txt in [
            (ACCENT,   "Aujourd'hui"),
            ("#14532d", "Congé approuvé"),
            ("#431407", "En attente"),
            (PANEL,    "Disponible"),
        ]:
            tk.Frame(leg, bg=color, width=18, height=14,
                     highlightthickness=1, highlightbackground=BORDER).pack(side="left", padx=4)
            _label(leg, txt, 9, False, MUTED, BG).pack(side="left", padx=(2, 16))

    def _prev_month(self):
        self.cal_month -= 1
        if self.cal_month < 1: self.cal_month = 12; self.cal_year -= 1
        self._render_calendar()

    def _next_month(self):
        self.cal_month += 1
        if self.cal_month > 12: self.cal_month = 1; self.cal_year += 1
        self._render_calendar()
