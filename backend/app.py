"""
Application principale : Vacation Manager
Initialise tous les services et la base de données
"""
import sys
import os
from datetime import datetime, timedelta

# Ajouter le répertoire backend au chemin Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Models import User, Employee, VacationRequest, VacationStatus
from Database import DatabaseManager
from Services import AuthService, EmployeeService, VacationService


class VacationManagerApp:
    """Application principale de gestion des congés."""

    def __init__(self, db_path: str = "vacation_manager.db"):
        """
        Initialise l'application.
        
        Args:
            db_path: Chemin à la base de données
        """
        self.db = DatabaseManager(db_path)
        self.auth_service = AuthService(self.db)
        self.employee_service = EmployeeService(self.db)
        self.vacation_service = VacationService(self.db)

    def test_authentication(self):
        """Teste l'authentification."""
        print("\n=== TEST D'AUTHENTIFICATION ===")
        
        # Connecter admin
        admin = self.auth_service.authenticate('admin@company.com', 'Azerty1234')
        print(f"Admin login: {'✓' if admin else '✗'}")
        if admin:
            print(f"  - ID: {admin.id}, Role: {admin.role}")

        # Connecter user
        user = self.auth_service.authenticate('user@company.com', 'Azerty1234')
        print(f"User login: {'✓' if user else '✗'}")
        if user:
            print(f"  - ID: {user.id}, Role: {user.role}")

        # Tentative de login échoué
        failed = self.auth_service.authenticate('user@company.com', 'WrongPassword')
        print(f"Failed login: {'✓' if not failed else '✗'}")

        return admin, user

    def test_employee_management(self):
        """Teste la gestion des employés."""
        print("\n=== GESTION DES EMPLOYÉS ===")

        # Récupérer l'employé par défaut
        employee = self.employee_service.get_employee_by_user_id(2)  # user_id = 2
        if employee:
            print(f"Employé trouvé: {employee.name}")
            print(f"  - Email: {employee.email}")
            print(f"  - Département: {employee.department}")
            print(f"  - Solde: {employee.vacation_balance} jours")
            print(f"  - Utilisé: {employee.vacation_used} jours")
            print(f"  - Disponible: {employee.get_vacation_available()} jours")

        return employee

    def test_vacation_request(self, employee):
        """Teste les demandes de congés."""
        print("\n=== DEMANDES DE CONGÉS ===")

        if not employee:
            print("Aucun employé disponible")
            return None

        # Créer une demande valide
        start = datetime.now() + timedelta(days=5)
        end = datetime.now() + timedelta(days=7)

        vacation_req = self.vacation_service.submit_vacation_request(
            employee.id,
            start,
            end,
            "Vacances familiales"
        )

        if vacation_req:
            print(f"Demande créée: #{vacation_req.id}")
            print(f"  - Dates: {vacation_req.start_date.date()} à {vacation_req.end_date.date()}")
            print(f"  - Jours: {vacation_req.days_count}")
            print(f"  - Statut: {vacation_req.status.value}")
            print(f"  - Motif: {vacation_req.reason}")
        else:
            print("Impossible de créer la demande")

        return vacation_req

    def test_approval_workflow(self, vacation_req):
        """Teste le flux d'approbation."""
        print("\n=== FLUX D'APPROBATION ===")

        if not vacation_req:
            print("Aucune demande disponible")
            return

        # Récupérer les demandes en attente
        pending = self.vacation_service.get_pending_vacation_requests()
        print(f"Demandes en attente: {len(pending)}")

        # Approuver la demande
        admin_id = 1  # Admin ID
        approved = self.vacation_service.approve_vacation_request(vacation_req.id, admin_id)
        print(f"Approbation: {'✓' if approved else '✗'}")

        if approved:
            updated = self.vacation_service.get_vacation_request(vacation_req.id)
            print(f"  - Nouveau statut: {updated.status.value}")
            print(f"  - Approuvé par: ID {updated.approved_by}")

            # Vérifier les congés utilisés
            employee = self.employee_service.get_employee(vacation_req.employee_id)
            print(f"  - Nouveaux jours utilisés: {employee.vacation_used}")
            print(f"  - Jours restants: {employee.get_vacation_available()}")

    def test_statistics(self, employee):
        """Teste les statistiques."""
        print("\n=== STATISTIQUES CONGÉS ===")

        stats = self.vacation_service.get_employee_vacation_statistics(employee.id)
        if stats:
            print(f"Solde total: {stats['total_balance']} jours")
            print(f"Utilisé: {stats['used_days']} jours")
            print(f"Disponible: {stats['available_days']} jours")
            print(f"Demandes en attente: {stats['pending_requests']} ({stats['pending_days']} jours)")
            print(f"Demandes approuvées: {stats['approved_requests']}")
            print(f"Demandes rejetées: {stats['rejected_requests']}")
            print(f"Total demandes: {stats['total_requests']}")

    def run_tests(self):
        """Lance tous les tests."""
        print("╔════════════════════════════════════════╗")
        print("║  APPLICATION VACATION MANAGER - TESTS  ║")
        print("╚════════════════════════════════════════╝")

        # Tests
        admin, user = self.test_authentication()
        employee = self.test_employee_management()
        vacation_req = self.test_vacation_request(employee)
        self.test_approval_workflow(vacation_req)
        if employee:
            self.test_statistics(employee)

        print("\n" + "="*40)
        print("Tests terminés!")
        print("="*40)


def main():
    """Fonction principale."""
    app = VacationManagerApp()
    app.run_tests()


if __name__ == "__main__":
    main()
