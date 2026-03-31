"""
Frontend Vacation Manager - Connected to Backend API
Interface GUI pour gérer les congés via API REST
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, tkcalendar
import requests
from datetime import datetime, date, timedelta
import threading
import json

API_URL = "http://localhost:5000/api"

class VacationManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Congés - HIY")
        self.root.geometry("900x700")
        
        self.current_user = None
        self.current_employee = None
        self.api_online = False
        
        # Vérifier la connexion API
        self.check_api_connection()
        
        if not self.api_online:
            messagebox.showerror("Erreur", "Impossible de se connecter à l'API backend.\nVérifiez que le serveur est démarré.")
            self.root.destroy()
            return
        
        # Créer l'interface de login
        self.show_login()
    
    def check_api_connection(self):
        """Vérifier si l'API est accessible."""
        try:
            response = requests.get(f"{API_URL}/health", timeout=2)
            self.api_online = response.status_code == 200
        except:
            self.api_online = False
    
    def show_login(self):
        """Afficher l'écran de login."""
        self.clear_window()
        
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre
        title = ttk.Label(frame, text="Vacation Manager - Login", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Email
        ttk.Label(frame, text="Email:").pack(anchor=tk.W, pady=(10, 5))
        self.email_entry = ttk.Entry(frame, width=40)
        self.email_entry.pack(pady=(0, 15))
        self.email_entry.insert(0, "admin@company.com")
        
        # Password
        ttk.Label(frame, text="Password:").pack(anchor=tk.W, pady=(10, 5))
        self.password_entry = ttk.Entry(frame, width=40, show="*")
        self.password_entry.pack(pady=(0, 20))
        self.password_entry.insert(0, "Azerty1234")
        
        # Login Button
        login_btn = ttk.Button(frame, text="Sign In", command=self.login)
        login_btn.pack(pady=20)
        
        # Info
        info = ttk.Label(frame, text="Identifiants de test:\nAdmin: admin@company.com\nUser: user@company.com\nMDP: Azerty1234", 
                        font=("Arial", 10), foreground="gray")
        info.pack(pady=20)
    
    def login(self):
        """Authentifier l'utilisateur."""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        try:
            response = requests.post(f"{API_URL}/login", json={
                "email": email,
                "password": password
            })
            
            if response.status_code == 200:
                data = response.json()
                self.current_user = data['user']
                
                # Récupérer l'employé
                emp_response = requests.get(f"{API_URL}/employees/{self.current_user['id']}")
                if emp_response.status_code == 200:
                    self.current_employee = emp_response.json()['employee']
                    self.show_dashboard()
                else:
                    messagebox.showerror("Erreur", "Impossible de récupérer les données employé")
            else:
                messagebox.showerror("Erreur", response.json()['message'])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(e)}")
    
    def show_dashboard(self):
        """Afficher le dashboard principal."""
        self.clear_window()
        
        # Header
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header, text=f"Bienvenue, {self.current_user['username']}", 
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        role_label = ttk.Label(header, text=f"Rôle: {self.current_user['role'].upper()}", 
                              font=("Arial", 10), foreground="blue")
        role_label.pack(side=tk.LEFT, padx=20)
        
        logout_btn = ttk.Button(header, text="Logout", command=self.logout)
        logout_btn.pack(side=tk.RIGHT)
        
        # Notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Dashboard
        dashboard_tab = ttk.Frame(notebook)
        notebook.add(dashboard_tab, text="Dashboard")
        self.create_dashboard_tab(dashboard_tab)
        
        # Tab 2: Vacation Requests
        vacations_tab = ttk.Frame(notebook)
        notebook.add(vacations_tab, text="Mes Demandes")
        self.create_vacations_tab(vacations_tab)
        
        # Tab 3: Admin (si admin)
        if self.current_user['role'] == 'admin':
            admin_tab = ttk.Frame(notebook)
            notebook.add(admin_tab, text="Admin")
            self.create_admin_tab(admin_tab)
    
    def create_dashboard_tab(self, parent):
        """Créer l'onglet dashboard."""
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Infos employé
        emp_frame = ttk.LabelFrame(frame, text="Vos Informations", padding=10)
        emp_frame.pack(fill=tk.X, pady=10)
        
        if self.current_employee:
            ttk.Label(emp_frame, text=f"Nom: {self.current_employee['name']}").grid(row=0, column=0, sticky=tk.W, pady=5)
            ttk.Label(emp_frame, text=f"Email: {self.current_employee['email']}").grid(row=1, column=0, sticky=tk.W, pady=5)
            ttk.Label(emp_frame, text=f"Département: {self.current_employee['department']}").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Statistiques congés
        stats_frame = ttk.LabelFrame(frame, text="Statistiques Congés", padding=10)
        stats_frame.pack(fill=tk.X, pady=10)
        
        if self.current_employee:
            ttk.Label(stats_frame, text=f"Solde Total: {self.current_employee['vacation_balance']} jours", 
                     font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
            ttk.Label(stats_frame, text=f"Utilisé: {self.current_employee['vacation_used']} jours").grid(row=0, column=1, padx=10, pady=5)
            ttk.Label(stats_frame, text=f"Disponible: {self.current_employee['vacation_balance'] - self.current_employee['vacation_used']} jours",
                     font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=5)
        
        # Bouton nouvelle demande
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=20)
        ttk.Button(btn_frame, text="Nouvelle Demande de Congés", command=self.show_new_vacation_form).pack(side=tk.LEFT, padx=5)
    
    def create_vacations_tab(self, parent):
        """Créer l'onglet demandes de congés."""
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Bouton rafraîchir
        ttk.Button(frame, text="Rafraîchir", command=lambda: self.refresh_vacations_tab(frame)).pack(pady=10)
        
        # Tableau
        self.refresh_vacations_tab(frame)
    
    def refresh_vacations_tab(self, parent):
        """Rafraîchir le tableau des demandes."""
        # Nettoyer le contenu
        for widget in parent.winfo_children()[1:]:
            widget.destroy()
        
        try:
            response = requests.get(f"{API_URL}/vacation-requests?user_id={self.current_user['id']}")
            if response.status_code == 200:
                requests_list = response.json()['vacation_requests']
                
                # Créer le tableau
                tree = ttk.Treeview(parent, columns=('Start', 'End', 'Days', 'Status', 'Reason'), 
                                   show='headings', height=10)
                tree.heading('Start', text='Début')
                tree.heading('End', text='Fin')
                tree.heading('Days', text='Jours')
                tree.heading('Status', text='Statut')
                tree.heading('Reason', text='Raison')
                
                tree.column('Start', width=100)
                tree.column('End', width=100)
                tree.column('Days', width=50)
                tree.column('Status', width=80)
                tree.column('Reason', width=200)
                
                for req in requests_list:
                    status_color = {
                        'PENDING': 'orange',
                        'APPROVED': 'green',
                        'REJECTED': 'red',
                        'CANCELLED': 'gray'
                    }.get(req['status'], 'black')
                    
                    tree.insert('', tk.END, values=(
                        req['start_date'][:10],
                        req['end_date'][:10],
                        req['days'],
                        req['status'],
                        req['reason']
                    ), tags=(status_color,))
                
                tree.tag_configure('orange', foreground='orange')
                tree.tag_configure('green', foreground='green')
                tree.tag_configure('red', foreground='red')
                tree.tag_configure('gray', foreground='gray')
                
                tree.pack(fill=tk.BOTH, expand=True, pady=10)
        except Exception as e:
            ttk.Label(parent, text=f"Erreur: {str(e)}").pack()
    
    def create_admin_tab(self, parent):
        """Créer l'onglet admin."""
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Employés
        ttk.Label(frame, text="Gestion des Employés", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Voir Employés", command=self.show_employees_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Ajouter Employé", command=self.show_add_employee_form).pack(side=tk.LEFT, padx=5)
        
        # Demandes en attente
        ttk.Label(frame, text="Demandes en Attente", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(20, 10))
        
        self.create_pending_requests_list(frame)
    
    def create_pending_requests_list(self, parent):
        """Afficher la liste des demandes en attente."""
        try:
            response = requests.get(f"{API_URL}/vacation-requests?status=PENDING")
            if response.status_code == 200:
                requests_list = response.json()['vacation_requests']
                
                if not requests_list:
                    ttk.Label(parent, text="Aucune demande en attente").pack()
                    return
                
                # Créer le tableau
                tree = ttk.Treeview(parent, columns=('Employee', 'Start', 'End', 'Days', 'Reason'), 
                                   show='headings', height=8)
                tree.heading('Employee', text='Employé')
                tree.heading('Start', text='Début')
                tree.heading('End', text='Fin')
                tree.heading('Days', text='Jours')
                tree.heading('Reason', text='Raison')
                
                tree.column('Employee', width=150)
                tree.column('Start', width=100)
                tree.column('End', width=100)
                tree.column('Days', width=50)
                tree.column('Reason', width=250)
                
                for req in requests_list:
                    tree.insert('', tk.END, values=(
                        f"Employé #{req['employee_id']}",
                        req['start_date'][:10],
                        req['end_date'][:10],
                        req['days'],
                        req['reason']
                    ))
                
                tree.pack(fill=tk.BOTH, expand=True, pady=10)
                
                # Actions
                actions_frame = ttk.Frame(parent)
                actions_frame.pack(fill=tk.X, pady=10)
                
                def approve_selected():
                    selected = tree.selection()
                    if selected:
                        idx = tree.index(selected[0])
                        req_id = requests_list[idx]['id']
                        self.approve_request(req_id)
                        self.create_pending_requests_list(parent)
                
                def reject_selected():
                    selected = tree.selection()
                    if selected:
                        idx = tree.index(selected[0])
                        req_id = requests_list[idx]['id']
                        self.reject_request(req_id)
                        self.create_pending_requests_list(parent)
                
                ttk.Button(actions_frame, text="Approuver", command=approve_selected).pack(side=tk.LEFT, padx=5)
                ttk.Button(actions_frame, text="Rejeter", command=reject_selected).pack(side=tk.LEFT, padx=5)
        except Exception as e:
            ttk.Label(parent, text=f"Erreur: {str(e)}").pack()
    
    def show_new_vacation_form(self):
        """Afficher le formulaire de nouvelle demande."""
        form_window = tk.Toplevel(self.root)
        form_window.title("Nouvelle Demande de Congés")
        form_window.geometry("400x400")
        
        frame = ttk.Frame(form_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Date début
        ttk.Label(frame, text="Date de Début:").grid(row=0, column=0, sticky=tk.W, pady=10)
        start_var = tk.StringVar(value=datetime.now().date().isoformat())
        start_entry = ttk.Entry(frame, textvariable=start_var, width=30)
        start_entry.grid(row=0, column=1, pady=10)
        
        # Date fin
        ttk.Label(frame, text="Date de Fin:").grid(row=1, column=0, sticky=tk.W, pady=10)
        end_var = tk.StringVar(value=(datetime.now().date() + timedelta(days=1)).isoformat())
        end_entry = ttk.Entry(frame, textvariable=end_var, width=30)
        end_entry.grid(row=1, column=1, pady=10)
        
        # Raison
        ttk.Label(frame, text="Raison:").grid(row=2, column=0, sticky=tk.W, pady=10)
        reason_text = tk.Text(frame, height=6, width=35)
        reason_text.grid(row=3, column=0, columnspan=2, pady=10)
        
        def submit():
            try:
                response = requests.post(f"{API_URL}/vacation-requests", json={
                    "employee_id": self.current_employee['id'],
                    "start_date": start_var.get(),
                    "end_date": end_var.get(),
                    "reason": reason_text.get("1.0", tk.END).strip()
                })
                
                if response.status_code == 201:
                    messagebox.showinfo("Succès", "Demande créée avec succès")
                    form_window.destroy()
                    self.show_dashboard()
                else:
                    messagebox.showerror("Erreur", response.json()['message'])
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        
        ttk.Button(frame, text="Soumettre", command=submit).grid(row=4, column=0, columnspan=2, pady=20)
    
    def show_employees_list(self):
        """Afficher la liste des employés."""
        list_window = tk.Toplevel(self.root)
        list_window.title("Employés")
        list_window.geometry("600x400")
        
        try:
            response = requests.get(f"{API_URL}/employees")
            if response.status_code == 200:
                employees = response.json()['employees']
                
                tree = ttk.Treeview(list_window, columns=('Name', 'Email', 'Department', 'Balance'), 
                                   show='headings')
                tree.heading('Name', text='Nom')
                tree.heading('Email', text='Email')
                tree.heading('Department', text='Département')
                tree.heading('Balance', text='Solde')
                
                tree.column('Name', width=150)
                tree.column('Email', width=150)
                tree.column('Department', width=150)
                tree.column('Balance', width=80)
                
                for emp in employees:
                    tree.insert('', tk.END, values=(
                        emp['name'],
                        emp['email'],
                        emp['department'],
                        emp['vacation_balance']
                    ))
                
                tree.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def show_add_employee_form(self):
        """Afficher le formulaire d'ajout d'employé."""
        form_window = tk.Toplevel(self.root)
        form_window.title("Ajouter Employé")
        form_window.geometry("400x300")
        
        frame = ttk.Frame(form_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Nom:").grid(row=0, column=0, sticky=tk.W, pady=10)
        name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=name_var, width=30).grid(row=0, column=1, pady=10)
        
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=10)
        email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=email_var, width=30).grid(row=1, column=1, pady=10)
        
        ttk.Label(frame, text="Département:").grid(row=2, column=0, sticky=tk.W, pady=10)
        dept_var = tk.StringVar()
        ttk.Entry(frame, textvariable=dept_var, width=30).grid(row=2, column=1, pady=10)
        
        def submit():
            messagebox.showinfo("Info", "Fonctionnalité non disponible dans cette version")
            form_window.destroy()
        
        ttk.Button(frame, text="Ajouter", command=submit).grid(row=3, column=0, columnspan=2, pady=20)
    
    def approve_request(self, req_id):
        """Approuver une demande."""
        try:
            response = requests.put(f"{API_URL}/vacation-requests/{req_id}/approve", json={
                "approved_by": "admin"
            })
            
            if response.status_code == 200:
                messagebox.showinfo("Succès", "Demande approuvée")
            else:
                messagebox.showerror("Erreur", response.json()['message'])
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def reject_request(self, req_id):
        """Rejeter une demande."""
        reason = simpledialog.askstring("Rejeter", "Raison du rejet:")
        if reason:
            try:
                response = requests.put(f"{API_URL}/vacation-requests/{req_id}/reject", json={
                    "reason": reason
                })
                
                if response.status_code == 200:
                    messagebox.showinfo("Succès", "Demande rejetée")
                else:
                    messagebox.showerror("Erreur", response.json()['message'])
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
    
    def logout(self):
        """Se déconnecter."""
        self.current_user = None
        self.current_employee = None
        self.show_login()
    
    def clear_window(self):
        """Vider la fenêtre."""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = VacationManagerGUI(root)
    root.mainloop()
