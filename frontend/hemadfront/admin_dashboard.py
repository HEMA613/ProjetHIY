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

STATUS_CFG = {
    "pending":  ("#451a03", "#f59e0b", "⏳ En attente"),
    "approved": ("#052e16", "#22c55e", "✅ Approuvé"),
    "rejected": ("#450a0a", "#ef4444", "❌ Refusé"),
}


def _label(parent, text, size=10, bold=False, fg=FG, bg=None, anchor="w"):
    bg = bg or parent.cget("bg")
    w = "bold" if bold else "normal"
    return tk.Label(parent, text=text, font=("Helvetica", size, w),
                    fg=fg, bg=bg, anchor=anchor)


class ManagerDashboard:
    def __init__(self, root, user):
        self.root    = root
        self.user    = user
        self.service = VacationService()
        self.cal_year  = date.today().year
        self.cal_month = date.today().month

        self.root.title(f"Management — {user['full_name']}")
        self.root.geometry("980x680")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self._center()
        self._build()

    def _center(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 980) // 2
        y = (self.root.winfo_screenheight() - 680) // 2
        self.root.geometry(f"980x680+{x}+{y}")

    # ── skeleton ──────────────────────────────────────────────
    def _build(self):
        # Header
        hdr = tk.Frame(self.root, bg=ACCENT, height=54)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        _label(hdr, "✦  Gestion des Congés  ·  Management", 13, True, FG, ACCENT).pack(side="left", padx=22, pady=14)
        _label(hdr, f"👤  {self.user['full_name']}", 10, False, "#c7d2fe", ACCENT).pack(side="right", padx=22)

        # Style notebook
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook",         background=BG,    borderwidth=0)
        style.configure("TNotebook.Tab",     background=PANEL, foreground=MUTED,
                        font=("Helvetica", 10), padding=[18, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", CARD)],
                  foreground=[("selected", FG)])

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        self.tab_req  = tk.Frame(nb, bg=BG); nb.add(self.tab_req,  text="  📋  Demandes  ")
        self.tab_cal  = tk.Frame(nb, bg=BG); nb.add(self.tab_cal,  text="  📅  Calendrier  ")
        self.tab_emp  = tk.Frame(nb, bg=BG); nb.add(self.tab_emp,  text="  👥  Employees  ")

        self._build_requests()
        self._build_calendar()
        self._build_employees()

    # ── TAB 1 : Demandes ─────────────────────────────────────
    def _build_requests(self):
        # Stats row
        stats_row = tk.Frame(self.tab_req, bg=BG)
        stats_row.pack(fill="x", padx=20, pady=(16, 8))

        vacs = self.service.get_all_vacations()
        for count, label, color in [
            (len([v for v in vacs if v["status"] == "pending"]),  "En attente", WARNING),
            (len([v for v in vacs if v["status"] == "approved"]), "Approuvés",  SUCCESS),
            (len([v for v in vacs if v["status"] == "rejected"]), "Refusés",    DANGER),
            (len(vacs),                                           "Total",      ACCENT),
        ]:
            c = tk.Frame(stats_row, bg=PANEL, bd=0)
            c.pack(side="left", padx=6, ipadx=22, ipady=10)
            _label(c, str(count), 26, True, color, PANEL, "center").pack()
            _label(c, label,      9,  False, MUTED, PANEL, "center").pack()

        # Filter bar
        flt = tk.Frame(self.tab_req, bg=BG)
        flt.pack(fill="x", padx=20, pady=(0, 6))
        _label(flt, "Filtrer :", 10, False, MUTED, BG).pack(side="left", padx=(0, 10))
        self.filter_var = tk.StringVar(value="all")
        for val, txt in [("all", "Tous"), ("pending", "En attente"), ("approved", "Approuvés"), ("rejected", "Refusés")]:
            rb = tk.Radiobutton(flt, text=txt, variable=self.filter_var, value=val,
                                command=self._refresh_req,
                                bg=BG, fg=MUTED, selectcolor=PANEL,
                                activebackground=BG, activeforeground=FG,
                                font=("Helvetica", 10))
            rb.pack(side="left", padx=8)

        # Treeview
        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background=PANEL, foreground=FG,
                        fieldbackground=PANEL, rowheight=32,
                        font=("Helvetica", 10))
        style.configure("Dark.Treeview.Heading",
                        background=CARD, foreground=MUTED,
                        font=("Helvetica", 10, "bold"), relief="flat")
        style.map("Dark.Treeview", background=[("selected", ACCENT)])

        cols = ("Employee", "Début", "Fin", "Durée", "Motif", "Soumis le", "Statut")
        frm  = tk.Frame(self.tab_req, bg=BG)
        frm.pack(fill="both", expand=True, padx=20, pady=4)

        self.tree = ttk.Treeview(frm, columns=cols, show="headings",
                                 style="Dark.Treeview", height=14)
        widths = [130, 100, 100, 70, 200, 100, 130]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        self.tree.tag_configure("pending",  background="#451a03", foreground="#fde68a")
        self.tree.tag_configure("approved", background="#052e16", foreground="#86efac")
        self.tree.tag_configure("rejected", background="#450a0a", foreground="#fca5a5")

        sb = ttk.Scrollbar(frm, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Action buttons
        btn_row = tk.Frame(self.tab_req, bg=BG)
        btn_row.pack(pady=12)
        tk.Button(btn_row, text="✅   Approuver", font=("Helvetica", 11, "bold"),
                  bg=SUCCESS, fg=BG, activebackground="#16a34a", relief="flat",
                  cursor="hand2", command=self._approve).pack(side="left", padx=12, ipadx=20, ipady=7)
        tk.Button(btn_row, text="❌   Refuser", font=("Helvetica", 11, "bold"),
                  bg=DANGER, fg=FG, activebackground="#dc2626", relief="flat",
                  cursor="hand2", command=self._reject).pack(side="left", padx=12, ipadx=20, ipady=7)

        self._refresh_req()

    def _refresh_req(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        vacs  = self.service.get_all_vacations()
        users = {u["username"]: u.get("full_name", u["username"]) for u in self.service.load_users()}
        flt   = self.filter_var.get()
        for v in reversed(vacs):
            if flt != "all" and v["status"] != flt:
                continue
            name   = users.get(v["username"], v["username"])
            days   = VacationService.count_days(v["start_date"], v["end_date"])
            _, _, slabel = STATUS_CFG.get(v["status"], ("", "", v["status"]))
            self.tree.insert("", "end", iid=str(v["id"]),
                             values=(name, v["start_date"], v["end_date"],
                                     f"{days}j", v.get("reason", "—"),
                                     v.get("submitted_date", "—"), slabel),
                             tags=(v["status"],))

    def _approve(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Attention", "Sélectionnez une demande.", parent=self.root); return
        self.service.update_status(int(sel[0]), "approved")
        messagebox.showinfo("Succès", "Congé approuvé ✅", parent=self.root)
        self._refresh_req(); self._refresh_employees()

    def _reject(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Attention", "Sélectionnez une demande.", parent=self.root); return
        self.service.update_status(int(sel[0]), "rejected")
        messagebox.showinfo("Info", "Congé refusé ❌", parent=self.root)
        self._refresh_req(); self._refresh_employees()

    # ── TAB 2 : Calendrier ───────────────────────────────────
    def _build_calendar(self):
        self._render_calendar()

    def _render_calendar(self):
        for w in self.tab_cal.winfo_children():
            w.destroy()

        # Nav
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

        day_names = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        for i, d in enumerate(day_names):
            fg = DANGER if i >= 5 else MUTED
            _label(grid, d, 10, True, fg, BG, "center").grid(row=0, column=i, padx=3, pady=4, sticky="ew")
            grid.grid_columnconfigure(i, weight=1)

        vacs     = self.service.get_all_vacations()
        users    = {u["username"]: u.get("full_name", u["username"]) for u in self.service.load_users()}
        approved = [v for v in vacs if v["status"] == "approved"]
        today    = date.today()

        for week_i, week in enumerate(calendar.monthcalendar(self.cal_year, self.cal_month), 1):
            for day_i, day in enumerate(week):
                if day == 0:
                    tk.Label(grid, text="", bg=BG).grid(row=week_i, column=day_i, padx=3, pady=3, sticky="nsew")
                    continue

                cur = date(self.cal_year, self.cal_month, day)
                on_vac = []
                for v in approved:
                    try:
                        if date.fromisoformat(v["start_date"]) <= cur <= date.fromisoformat(v["end_date"]):
                            name = users.get(v["username"], v["username"])
                            on_vac.append(name.split()[0])
                    except Exception:
                        pass

                is_today   = cur == today
                is_weekend = day_i >= 5

                if is_today:
                    bg, num_fg = ACCENT, FG
                elif on_vac:
                    bg, num_fg = "#1e3a5f", "#93c5fd"
                elif is_weekend:
                    bg, num_fg = "#0d1b2a", MUTED
                else:
                    bg, num_fg = PANEL, FG

                cell = tk.Frame(grid, bg=bg, bd=0, highlightthickness=1,
                                highlightbackground=BORDER)
                cell.grid(row=week_i, column=day_i, padx=3, pady=3, sticky="nsew")
                grid.grid_rowconfigure(week_i, weight=1)

                _label(cell, str(day), 11, True, num_fg, bg).pack(anchor="nw", padx=5, pady=(4, 0))
                if on_vac:
                    names = ", ".join(on_vac[:2])
                    if len(on_vac) > 2:
                        names += f" +{len(on_vac)-2}"
                    _label(cell, names, 8, False, "#93c5fd", bg).pack(anchor="w", padx=5)

        # Legend
        leg = tk.Frame(self.tab_cal, bg=BG)
        leg.pack(pady=10)
        for color, txt in [(ACCENT, "Aujourd'hui"), ("#1e3a5f", "En congé"), (PANEL, "Disponible")]:
            tk.Frame(leg, bg=color, width=18, height=14, bd=1,
                     highlightthickness=1, highlightbackground=BORDER).pack(side="left", padx=4)
            _label(leg, txt, 9, False, MUTED, BG).pack(side="left", padx=(2, 14))

    def _prev_month(self):
        self.cal_month -= 1
        if self.cal_month < 1: self.cal_month = 12; self.cal_year -= 1
        self._render_calendar()

    def _next_month(self):
        self.cal_month += 1
        if self.cal_month > 12: self.cal_month = 1; self.cal_year += 1
        self._render_calendar()

    # ── TAB 3 : Employees ─────────────────────────────────────
    def _build_employees(self):
        self.emp_scroll_frame = tk.Frame(self.tab_emp, bg=BG)
        self.emp_scroll_frame.pack(fill="both", expand=True, padx=24, pady=16)
        self._refresh_employees()

    def _refresh_employees(self):
        for w in self.emp_scroll_frame.winfo_children():
            w.destroy()

        _label(self.emp_scroll_frame, "Vue d'ensemble des employees",
               14, True, FG, BG).pack(anchor="w", pady=(0, 12))

        users = [u for u in self.service.load_users() if u["role"] == "employee"]
        for u in users:
            total     = u.get("total_days", 25)
            used      = self.service.get_used_days(u["username"])
            remaining = total - used
            pct       = max(0.0, min(1.0, used / total)) if total else 0

            bar_color = SUCCESS if pct < 0.6 else WARNING if pct < 0.85 else DANGER

            card = tk.Frame(self.emp_scroll_frame, bg=PANEL, bd=0,
                            highlightthickness=1, highlightbackground=BORDER)
            card.pack(fill="x", pady=6, ipady=6)

            top = tk.Frame(card, bg=PANEL)
            top.pack(fill="x", padx=16, pady=(10, 4))
            _label(top, u.get("full_name", u["username"]), 13, True, FG, PANEL).pack(side="left")
            _label(top, f"{remaining} / {total} jours restants", 10, False,
                   bar_color, PANEL).pack(side="right")

            # Progress bar background
            bar_bg = tk.Frame(card, bg=BORDER, height=8)
            bar_bg.pack(fill="x", padx=16, pady=(2, 6))
            bar_bg.update_idletasks()
            bar_fill = tk.Frame(bar_bg, bg=bar_color, height=8)
            bar_fill.place(relwidth=pct, relheight=1)

            # Demandes summary
            my_vacs = self.service.get_user_vacations(u["username"])
            pending  = len([v for v in my_vacs if v["status"] == "pending"])
            approved = len([v for v in my_vacs if v["status"] == "approved"])
            rejected = len([v for v in my_vacs if v["status"] == "rejected"])
            _label(card,
                   f"  ⏳ {pending} en attente   ✅ {approved} approuvés   ❌ {rejected} refusés   |   {used} jours consommés",
                   9, False, MUTED, PANEL).pack(anchor="w", padx=16, pady=(0, 6))
