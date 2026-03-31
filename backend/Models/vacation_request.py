"""
Module VacationRequest: Gestion des demandes de congés
"""
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional


class VacationStatus(Enum):
    """Énumération des statuts de demande de congés."""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


@dataclass
class VacationRequest:
    """
    Classe représentant une demande de congés.
    Attributs:
        id (int): Identifiant unique
        employee_id (int): ID de l'employé
        start_date (datetime): Date de début
        end_date (datetime): Date de fin
        reason (str): Motif de la demande
        status (VacationStatus): Statut de la demande
        days_count (int): Nombre de jours calculés
        created_at (datetime): Date de création
        updated_at (datetime): Date de dernière modification
        approved_by (int): ID de l'admin qui a approuvé (optionnel)
        rejection_reason (str): Motif du rejet (optionnel)
    """
    id: int
    employee_id: int
    start_date: datetime
    end_date: datetime
    reason: str
    status: VacationStatus = VacationStatus.PENDING
    days_count: int = 0
    created_at: datetime = None
    updated_at: datetime = None
    approved_by: Optional[int] = None
    rejection_reason: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.days_count == 0:
            self.days_count = self.calculate_days()

    def calculate_days(self) -> int:
        """Calcule le nombre de jours de congés."""
        if isinstance(self.start_date, str):
            start = datetime.fromisoformat(self.start_date).date()
        else:
            start = self.start_date.date() if isinstance(self.start_date, datetime) else self.start_date

        if isinstance(self.end_date, str):
            end = datetime.fromisoformat(self.end_date).date()
        else:
            end = self.end_date.date() if isinstance(self.end_date, datetime) else self.end_date

        delta = end - start
        return delta.days + 1  # Inclut les deux jours

    def is_valid(self) -> bool:
        """Vérifie que la demande est valide."""
        # Convertir en dates si nécessaire
        start = self.start_date.date() if isinstance(self.start_date, datetime) else self.start_date
        end = self.end_date.date() if isinstance(self.end_date, datetime) else self.end_date

        # Les dates ne doivent pas être dans le passé
        if start < datetime.now().date():
            return False
        # La date de début doit être avant la date de fin
        if start >= end:
            return False
        # Au moins 1 jour
        if self.days_count < 1:
            return False
        return True

    def approve(self, admin_id: int):
        """Approuve la demande."""
        self.status = VacationStatus.APPROVED
        self.approved_by = admin_id
        self.updated_at = datetime.now()

    def reject(self, reason: str):
        """Rejette la demande."""
        self.status = VacationStatus.REJECTED
        self.rejection_reason = reason
        self.updated_at = datetime.now()

    def cancel(self):
        """Annule la demande."""
        self.status = VacationStatus.CANCELLED
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict:
        """Convertit la demande en dictionnaire."""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'start_date': self.start_date.isoformat() if isinstance(self.start_date, datetime) else self.start_date,
            'end_date': self.end_date.isoformat() if isinstance(self.end_date, datetime) else self.end_date,
            'reason': self.reason,
            'status': self.status.value,
            'days_count': self.days_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'approved_by': self.approved_by,
            'rejection_reason': self.rejection_reason
        }

    @staticmethod
    def from_dict(data: Dict) -> 'VacationRequest':
        """Crée une demande de congés à partir d'un dictionnaire."""
        return VacationRequest(
            id=data.get('id'),
            employee_id=data.get('employee_id'),
            start_date=datetime.fromisoformat(data['start_date']) if isinstance(data.get('start_date'), str) else data.get('start_date'),
            end_date=datetime.fromisoformat(data['end_date']) if isinstance(data.get('end_date'), str) else data.get('end_date'),
            reason=data.get('reason'),
            status=VacationStatus(data.get('status', 'PENDING')),
            days_count=data.get('days_count', 0),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            approved_by=data.get('approved_by'),
            rejection_reason=data.get('rejection_reason')
        )
