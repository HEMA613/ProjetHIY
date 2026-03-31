"""
Module VacationService: Service de gestion des demandes de congés
"""
from datetime import datetime
from typing import Optional, List, Dict
from Models import VacationRequest, VacationStatus
from Database import DatabaseManager


class VacationService:
    """
    Service de gestion des demandes de congés.
    Gère la création, l'approbation et le suivi des demandes de congés.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialise le service de congés.
        
        Args:
            db_manager: Instance du gestionnaire de base de données
        """
        self.db = db_manager

    def submit_vacation_request(self, employee_id: int, start_date: datetime, end_date: datetime, reason: str) -> Optional[VacationRequest]:
        """
        Soumet une demande de congés.
        
        Args:
            employee_id: ID de l'employé
            start_date: Date de début
            end_date: Date de fin
            reason: Motif de la demande
            
        Returns:
            La demande créée ou None si échec
        """
        # Créer la demande
        vacation_request = VacationRequest(
            id=None,
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )

        # Valider la demande
        if not vacation_request.is_valid():
            return None

        # Vérifier si l'employé a assez de congés
        employee = self.db.get_employee_by_id(employee_id)
        if not employee or not employee.has_enough_balance(vacation_request.days_count):
            return None

        # Créer la demande en base de données
        return self.db.create_vacation_request(vacation_request)

    def get_vacation_request(self, request_id: int) -> Optional[VacationRequest]:
        """Récupère une demande de congés par ID."""
        return self.db.get_vacation_request_by_id(request_id)

    def get_employee_vacation_requests(self, employee_id: int) -> List[VacationRequest]:
        """Récupère toutes les demandes d'un employé."""
        return self.db.get_vacation_requests_by_employee(employee_id)

    def get_pending_vacation_requests(self) -> List[VacationRequest]:
        """Récupère toutes les demandes en attente d'approbation."""
        return self.db.get_all_pending_vacation_requests()

    def get_all_vacation_requests(self) -> List[VacationRequest]:
        """Récupère toutes les demandes de congés."""
        return self.db.get_all_vacation_requests()

    def approve_vacation_request(self, request_id: int, admin_id: int) -> bool:
        """
        Approuve une demande de congés.
        
        Args:
            request_id: ID de la demande
            admin_id: ID de l'administrateur qui approuve
            
        Returns:
            True si succès, False sinon
        """
        vacation_request = self.db.get_vacation_request_by_id(request_id)
        if not vacation_request or vacation_request.status != VacationStatus.PENDING:
            return False

        # Utiliser les jours de congés
        if not self.db.get_employee_by_id(vacation_request.employee_id):
            return False

        # Mettre à jour le statut
        self.db.update_vacation_request_status(
            request_id,
            VacationStatus.APPROVED,
            approved_by=admin_id
        )

        # Utiliser les jours de congés de l'employé
        employee = self.db.get_employee_by_id(vacation_request.employee_id)
        if employee:
            employee.use_vacation_days(vacation_request.days_count)
            self.db.update_employee_vacation(vacation_request.employee_id, employee.vacation_used)

        return True

    def reject_vacation_request(self, request_id: int, reason: str) -> bool:
        """
        Rejette une demande de congés.
        
        Args:
            request_id: ID de la demande
            reason: Motif du rejet
            
        Returns:
            True si succès, False sinon
        """
        vacation_request = self.db.get_vacation_request_by_id(request_id)
        if not vacation_request or vacation_request.status != VacationStatus.PENDING:
            return False

        # Mettre à jour le statut
        self.db.update_vacation_request_status(
            request_id,
            VacationStatus.REJECTED,
            rejection_reason=reason
        )

        return True

    def cancel_vacation_request(self, request_id: int) -> bool:
        """
        Annule une demande de congés (dans le cas d'une demande approuvée).
        
        Args:
            request_id: ID de la demande
            
        Returns:
            True si succès, False sinon
        """
        vacation_request = self.db.get_vacation_request_by_id(request_id)
        if not vacation_request:
            return False

        # Si la demande est approuvée, rembourser les jours
        if vacation_request.status == VacationStatus.APPROVED:
            employee = self.db.get_employee_by_id(vacation_request.employee_id)
            if employee:
                employee.refund_vacation_days(vacation_request.days_count)
                self.db.update_employee_vacation(vacation_request.employee_id, employee.vacation_used)

        # Mettre à jour le statut
        self.db.update_vacation_request_status(
            request_id,
            VacationStatus.CANCELLED
        )

        return True

    def get_vacation_request_details(self, request_id: int) -> Optional[Dict]:
        """Récupère les détails d'une demande de congés."""
        vacation_request = self.db.get_vacation_request_by_id(request_id)
        if not vacation_request:
            return None

        employee = self.db.get_employee_by_id(vacation_request.employee_id)
        approver = None
        if vacation_request.approved_by:
            approver = self.db.get_user_by_id(vacation_request.approved_by)

        return {
            'id': vacation_request.id,
            'employee': {
                'id': employee.id,
                'name': employee.name,
                'department': employee.department
            } if employee else None,
            'start_date': vacation_request.start_date.isoformat(),
            'end_date': vacation_request.end_date.isoformat(),
            'days_count': vacation_request.days_count,
            'reason': vacation_request.reason,
            'status': vacation_request.status.value,
            'created_at': vacation_request.created_at.isoformat(),
            'updated_at': vacation_request.updated_at.isoformat(),
            'approved_by': approver.username if approver else None,
            'rejection_reason': vacation_request.rejection_reason
        }

    def get_employee_vacation_statistics(self, employee_id: int) -> Optional[Dict]:
        """Récupère les statistiques de congés d'un employé."""
        employee = self.db.get_employee_by_id(employee_id)
        if not employee:
            return None

        requests = self.db.get_vacation_requests_by_employee(employee_id)

        approved_days = sum(
            req.days_count for req in requests
            if req.status == VacationStatus.APPROVED
        )

        pending_days = sum(
            req.days_count for req in requests
            if req.status == VacationStatus.PENDING
        )

        return {
            'total_balance': employee.vacation_balance,
            'used_days': employee.vacation_used,
            'available_days': employee.get_vacation_available(),
            'pending_requests': sum(1 for req in requests if req.status == VacationStatus.PENDING),
            'pending_days': pending_days,
            'approved_requests': sum(1 for req in requests if req.status == VacationStatus.APPROVED),
            'rejected_requests': sum(1 for req in requests if req.status == VacationStatus.REJECTED),
            'total_requests': len(requests)
        }
