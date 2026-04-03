import tkinter as tk
from tkinter import ttk, messagebox
from services.vacation_service import VacationService

class VacationApp:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.service = VacationService()

        self.root.title("Gestion Congés")
        self.create_menu()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        vac_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Congés", menu=vac_menu)
        vac_menu.add_command(label="Demander", command=self.request)

        if self.user["role"] == "admin":
            vac_menu.add_command(label="Valider", command=self.validate)

    def request(self):
        messagebox.showinfo("Info", "Demande envoyée (simulation)")

    def validate(self):
        messagebox.showinfo("Admin", "Validation des congés")
