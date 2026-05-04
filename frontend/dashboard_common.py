import os
import sys
import tkinter as tk
from tkinter import ttk

# Ajoute le dossier services au chemin Python si nécessaire.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
services_dir = os.path.join(BASE_DIR, "frontend", "services")
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

# Couleurs utilisées dans les dashboards.
BG = "#0f172a"
PANEL = "#1e293b"
CARD = "#263348"
ACCENT = "#6366f1"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"
DANGER = "#ef4444"
FG = "#f8fafc"
MUTED = "#94a3b8"
BORDER = "#334155"
ENTRY = "#0f172a"

STATUS_CFG = {
    "pending": ("#451a03", "#f59e0b", "⏳ En attente"),
    "approved": ("#052e16", "#22c55e", "✅ Approuvé"),
    "rejected": ("#450a0a", "#ef4444", "❌ Refusé"),
}


def _label(parent, text, size=10, bold=False, fg=FG, bg=None, anchor="w"):
    """Crée simplement un Label Tkinter avec des options propres."""
    bg = bg or parent.cget("bg")
    weight = "bold" if bold else "normal"
    return tk.Label(
        parent,
        text=text,
        font=("Helvetica", size, weight),
        fg=fg,
        bg=bg,
        anchor=anchor,
    )


def setup_notebook_style():
    """Configure le style du notebook (onglets) pour tous les dashboards."""
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=PANEL,
        foreground=MUTED,
        font=("Helvetica", 10),
        padding=[18, 8],
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", CARD)],
        foreground=[("selected", FG)],
    )
