"""
Module EmployeeService: Service de gestion des employés
"""
from typing import Optional, List
from Models import Employee, User
from Database import DatabaseManager


class EmployeeService:
    """
    Service de gestion des employés.
    Gère les profils, les soldes de congés et les données des employés.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialise le service d'employés.
        
        Args:
            db_manager: Instance du gestionnaire de base de données
        """
        self.db = db_manager

    def create_employee(self, user_id: int, name: str, email: str, department: str, position: str) -> Optional[Employee]:
        """
        Crée un profil d'employé.
        
        Args:
            user_id: ID de l'utilisateur associé
            name: Nom complet
            email: Email professionnel
            department: Département
            position: Poste
            
        Returns:
            L'employé créé ou None si échec
        """
        return self.db.create_employee(user_id, name, email, department, position)

    def get_employee(self, employee_id: int) -> Optional[Employee]:
        """Récupère un employé par ID."""
        return self.db.get_employee_by_id(employee_id)

    def get_employee_by_user_id(self, user_id: int) -> Optional[Employee]:
        """Récupère un employé par ID utilisateur."""
        return self.db.get_employee_by_user_id(user_id)

    def get_all_employees(self) -> List[Employee]:
        """Récupère tous les employés."""
        return self.db.get_all_employees()

    def get_vacation_balance(self, employee_id: int) -> Optional[int]:
        """Récupère le solde de congés d'un employé."""
        employee = self.db.get_employee_by_id(employee_id)
        if employee:
            return employee.get_vacation_available()
        return None

    def get_vacation_details(self, employee_id: int) -> Optional[dict]:
        """Récupère les détails des congés d'un employé."""
        employee = self.db.get_employee_by_id(employee_id)
        if employee:
            return {
                'total_balance': employee.vacation_balance,
                'days_used': employee.vacation_used,
                'days_available': employee.get_vacation_available()
            }
        return None

    def use_vacation_days(self, employee_id: int, days: int) -> bool:
        """Utilise des jours de congés pour un employé."""
        employee = self.db.get_employee_by_id(employee_id)
        if employee and employee.use_vacation_days(days):
            self.db.update_employee_vacation(employee_id, employee.vacation_used)
            return True
        return False

    def refund_vacation_days(self, employee_id: int, days: int) -> bool:
        """Rembourse des jours de congés (annulation)."""
        employee = self.db.get_employee_by_id(employee_id)
        if employee:
            employee.refund_vacation_days(days)
            self.db.update_employee_vacation(employee_id, employee.vacation_used)
            return True
        return False

    def has_enough_vacation(self, employee_id: int, days_requested: int) -> bool:
        """Vérifie si l'employé a assez de congés."""
        employee = self.db.get_employee_by_id(employee_id)
        if employee:
            return employee.has_enough_balance(days_requested)
        return False

    def get_employee_info(self, employee_id: int) -> Optional[dict]:
        """Récupère les informations complètes d'un employé."""
        employee = self.db.get_employee_by_id(employee_id)
        if employee:
            user = self.db.get_user_by_id(employee.user_id)
            return {
                'id': employee.id,
                'user_id': employee.user_id,
                'name': employee.name,
                'email': employee.email,
                'department': employee.department,
                'position': employee.position,
                'username': user.username if user else None,
                'vacation_balance': employee.vacation_balance,
                'vacation_used': employee.vacation_used,
                'vacation_available': employee.get_vacation_available(),
                'hire_date': employee.hire_date.isoformat() if employee.hire_date else None
            }
        return None
