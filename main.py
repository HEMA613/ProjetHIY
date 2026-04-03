import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, date
import calendar
class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x150")

        tk.Label(self, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Simulate authentication (replace with real logic)
        if username == "admin" and password == "password":
            messagebox.showinfo("Success", "Login successful!")
            self.destroy()
            # TODO: call main app
        else:
            messagebox.showerror("Error", "Invalid credentials")

if __name__ == "__main__":
    app = LoginForm()
    app.mainloop()

class VacationManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Congés - HIY")
        self.root.geometry("800x600")

        # Fichiers de données
        self.employees_file = 'employees.json'
        self.vacations_file = 'vacations.json'

        # Charger les données
        self.employees = self.load_employees()
        self.vacations = self.load_vacations()

        # Interface
        self.create_menu()
        self.create_dashboard()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Employés
        employees_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Employés", menu=employees_menu)
        employees_menu.add_command(label="Voir Employés", command=self.show_employees)
        employees_menu.add_command(label="Ajouter Employé", command=self.add_employee)

        # Menu Congés
        vacations_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Congés", menu=vacations_menu)
        vacations_menu.add_command(label="Demander Congé", command=self.request_vacation)
        vacations_menu.add_command(label="Voir Demandes", command=self.show_vacations)
        vacations_menu.add_command(label="Calendrier", command=self.show_calendar)

    def create_dashboard(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Titre
        title = ttk.Label(self.main_frame, text="Système de Gestion des Congés - HIY", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Statistiques
        stats_frame = ttk.Frame(self.main_frame)
        stats_frame.pack(pady=10)

        # Nombre d'employés
        employees_count = len(self.employees)
        ttk.Label(stats_frame, text=f"Nombre d'Employés: {employees_count}", font=("Arial", 12)).grid(row=0, column=0, padx=20)

        # Demandes en attente
        pending_count = len([v for v in self.vacations if v['status'] == 'pending'])
        ttk.Label(stats_frame, text=f"Demandes en Attente: {pending_count}", font=("Arial", 12)).grid(row=0, column=1, padx=20)

        # Congés approuvés
        approved_count = len([v for v in self.vacations if v['status'] == 'approved'])
        ttk.Label(stats_frame, text=f"Congés Approuvés: {approved_count}", font=("Arial", 12)).grid(row=0, column=2, padx=20)

    def load_employees(self):
        if os.path.exists(self.employees_file):
            with open(self.employees_file, 'r') as f:
                return json.load(f)
        # Employés par défaut
        return [
            {'id': 1, 'name': 'SUTHAHER Hemadhuran'},
            {'id': 2, 'name': 'ALI YOUSSOUF'},
        
        ]

    def save_employees(self):
        with open(self.employees_file, 'w') as f:
            json.dump(self.employees, f, indent=4)

    def load_vacations(self):
        if os.path.exists(self.vacations_file):
            with open(self.vacations_file, 'r') as f:
                return json.load(f)
        return []

    def save_vacations(self):
        with open(self.vacations_file, 'w') as f:
            json.dump(self.vacations, f, indent=4)

    def show_employees(self):
        # Nouvelle fenêtre
        employees_window = tk.Toplevel(self.root)
        employees_window.title("Gestion des Employés")
        employees_window.geometry("600x400")

        # Liste des employés
        tree = ttk.Treeview(employees_window, columns=('ID', 'Nom'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Nom', text='Nom')
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for emp in self.employees:
            tree.insert('', tk.END, values=(emp['id'], emp['name']))

        # Boutons
        btn_frame = ttk.Frame(employees_window)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Ajouter", command=self.add_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Supprimer", command=lambda: self.delete_employee(tree)).pack(side=tk.LEFT, padx=5)

    def add_employee(self):
        name = simpledialog.askstring("Ajouter Employé", "Nom de l'employé:")
        if name:
            new_id = max([e['id'] for e in self.employees]) + 1 if self.employees else 1
            self.employees.append({'id': new_id, 'name': name})
            self.save_employees()
            messagebox.showinfo("Succès", "Employé ajouté avec succès!")
            self.refresh_dashboard()

    def delete_employee(self, tree):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            emp_id = item['values'][0]
            self.employees = [e for e in self.employees if e['id'] != emp_id]
            self.save_employees()
            tree.delete(selected[0])
            messagebox.showinfo("Succès", "Employé supprimé!")
            self.refresh_dashboard()

    def request_vacation(self):
        # Nouvelle fenêtre
        req_window = tk.Toplevel(self.root)
        req_window.title("Demander un Congé")
        req_window.geometry("400x300")

        # Formulaire
        ttk.Label(req_window, text="Employé:").pack(pady=5)
        emp_var = tk.StringVar()
        emp_combo = ttk.Combobox(req_window, textvariable=emp_var, values=[e['name'] for e in self.employees])
        emp_combo.pack(pady=5)

        ttk.Label(req_window, text="Date de début (YYYY-MM-DD):").pack(pady=5)
        start_var = tk.StringVar()
        start_entry = ttk.Entry(req_window, textvariable=start_var)
        start_entry.pack(pady=5)

        ttk.Label(req_window, text="Date de fin (YYYY-MM-DD):").pack(pady=5)
        end_var = tk.StringVar()
        end_entry = ttk.Entry(req_window, textvariable=end_var)
        end_entry.pack(pady=5)

        ttk.Label(req_window, text="Raison:").pack(pady=5)
        reason_var = tk.StringVar()
        reason_entry = ttk.Entry(req_window, textvariable=reason_var)
        reason_entry.pack(pady=5)

        def submit():
            if not all([emp_var.get(), start_var.get(), end_var.get()]):
                messagebox.showerror("Erreur", "Tous les champs sont requis!")
                return

            emp_id = next(e['id'] for e in self.employees if e['name'] == emp_var.get())
            new_vacation = {
                'id': len(self.vacations) + 1,
                'employee_id': emp_id,
                'start_date': start_var.get(),
                'end_date': end_var.get(),
                'reason': reason_var.get(),
                'status': 'pending'
            }
            self.vacations.append(new_vacation)
            self.save_vacations()
            messagebox.showinfo("Succès", "Demande de congé soumise!")
            req_window.destroy()
            self.refresh_dashboard()

        ttk.Button(req_window, text="Soumettre", command=submit).pack(pady=10)

    def show_vacations(self):
        # Nouvelle fenêtre
        vac_window = tk.Toplevel(self.root)
        vac_window.title("Demandes de Congé")
        vac_window.geometry("800x400")

        # Liste des demandes
        tree = ttk.Treeview(vac_window, columns=('Employé', 'Début', 'Fin', 'Raison', 'Statut'), show='headings')
        tree.heading('Employé', text='Employé')
        tree.heading('Début', text='Date Début')
        tree.heading('Fin', text='Date Fin')
        tree.heading('Raison', text='Raison')
        tree.heading('Statut', text='Statut')
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for vac in self.vacations:
            emp_name = next(e['name'] for e in self.employees if e['id'] == vac['employee_id'])
            tree.insert('', tk.END, values=(emp_name, vac['start_date'], vac['end_date'], vac['reason'], vac['status']))

        # Boutons
        btn_frame = ttk.Frame(vac_window)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Approuver", command=lambda: self.approve_vacation(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Rejeter", command=lambda: self.reject_vacation(tree)).pack(side=tk.LEFT, padx=5)

    def approve_vacation(self, tree):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            values = item['values']
            emp_name = values[0]
            start_date = values[1]
            # Trouver la demande
            for vac in self.vacations:
                emp_id = next(e['id'] for e in self.employees if e['name'] == emp_name)
                if vac['employee_id'] == emp_id and vac['start_date'] == start_date:
                    vac['status'] = 'approved'
                    break
            self.save_vacations()
            tree.item(selected[0], values=(values[0], values[1], values[2], values[3], 'approved'))
            messagebox.showinfo("Succès", "Congé approuvé!")
            self.refresh_dashboard()

    def reject_vacation(self, tree):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            values = item['values']
            emp_name = values[0]
            start_date = values[1]
            # Trouver la demande
            for vac in self.vacations:
                emp_id = next(e['id'] for e in self.employees if e['name'] == emp_name)
                if vac['employee_id'] == emp_id and vac['start_date'] == start_date:
                    vac['status'] = 'rejected'
                    break
            self.save_vacations()
            tree.item(selected[0], values=(values[0], values[1], values[2], values[3], 'rejected'))
            messagebox.showinfo("Succès", "Congé rejeté!")
            self.refresh_dashboard()

    def show_calendar(self):
        # Nouvelle fenêtre
        cal_window = tk.Toplevel(self.root)
        cal_window.title("Calendrier des Congés")
        cal_window.geometry("600x400")

        # Calendrier simple pour le mois actuel
        now = datetime.now()
        year = now.year
        month = now.month

        # Titre du mois
        ttk.Label(cal_window, text=f"{calendar.month_name[month]} {year}", font=("Arial", 14, "bold")).pack(pady=10)

        # Grille du calendrier
        cal_frame = ttk.Frame(cal_window)
        cal_frame.pack(pady=10)

        # Jours de la semaine
        days = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
        for i, day in enumerate(days):
            ttk.Label(cal_frame, text=day, font=("Arial", 10, "bold")).grid(row=0, column=i, padx=5, pady=5)

        # Dates
        cal = calendar.monthcalendar(year, month)
        approved_vacations = [v for v in self.vacations if v['status'] == 'approved']

        for week_num, week in enumerate(cal, 1):
            for day_num, day in enumerate(week):
                if day == 0:
                    ttk.Label(cal_frame, text="").grid(row=week_num, column=day_num, padx=5, pady=5)
                else:
                    # Vérifier si quelqu'un est en congé ce jour
                    vacation_employees = []
                    for vac in approved_vacations:
                        start = date.fromisoformat(vac['start_date'])
                        end = date.fromisoformat(vac['end_date'])
                        current = date(year, month, day)
                        if start <= current <= end:
                            emp_name = next(e['name'] for e in self.employees if e['id'] == vac['employee_id'])
                            vacation_employees.append(emp_name[:3])  # Abréger

                    text = str(day)
                    if vacation_employees:
                        text += f"\n{', '.join(vacation_employees)}"

                    ttk.Label(cal_frame, text=text, anchor="nw").grid(row=week_num, column=day_num, padx=5, pady=5, sticky="nw")

    def refresh_dashboard(self):
        # Recréer le dashboard
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.create_dashboard()

if __name__ == "__main__":
    root = tk.Tk()
    app = VacationManager(root)
    root.mainloop()

    from datetime import date
from models.employee import Employee
from services.request_service import RequestService

employee = Employee(1, "Sarah", "sarah@test.com", "EMPLOYEE", 10)

service = RequestService()

request = service.submit_request(
    employee,
    1,
    date(2026, 4, 10),
    date(2026, 4, 12),
    "Family vacation"
)

print(request)
