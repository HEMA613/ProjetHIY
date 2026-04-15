import tkinter as tk
from tkinter import messagebox
from logic import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestion des congés")
        self.geometry("300x200")

        tk.Label(self, text="Email").pack()
        self.email = tk.Entry(self)
        self.email.pack()

        tk.Label(self, text="Password").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Button(self, text="Connexion", command=self.login).pack(pady=10)

    def login(self):
        user = login(self.email.get(), self.password.get())

        if user:
            messagebox.showinfo("OK", f"Bienvenue {user['nom']}")
            self.destroy()
            menu(user)
        else:
            messagebox.showerror("Erreur", "Identifiants faux")


def menu(user):
    win = tk.Tk()
    win.title("Menu")

    tk.Label(win, text=f"{user['nom']}").pack()

    tk.Button(win, text="Nouvelle demande",
              command=lambda: nouvelle_demande(user)).pack()

    win.mainloop()


def nouvelle_demande(user):
    win = tk.Toplevel()

    tk.Label(win, text="Date début").pack()
    d1 = tk.Entry(win)
    d1.pack()

    tk.Label(win, text="Date fin").pack()
    d2 = tk.Entry(win)
    d2.pack()

    def envoyer():
        res = soumettre_demande(
            user["id"], user["nom"], d1.get(), d2.get()
        )

        if res:
            messagebox.showinfo("OK", "Envoyé")
        else:
            messagebox.showerror("Erreur", "Refus")

    tk.Button(win, text="Envoyer", command=envoyer).pack()