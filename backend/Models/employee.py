"""
Module Employee: Gestion des employés et leurs données
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass
class Employee:
    """
    Classe représentant un employé du système.
    Attributs:
        id (int): Identifiant unique
        user_id (int): ID de l'utilisateur associé
        name (str): Nom complet
        email (str): Email professionnel
        department (str): Département
        position (str): Poste
        vacation_balance (int): Solde de congés en jours
        vacation_used (int): Jours de congés utilisés
        hire_date (datetime): Date d'embauche
        created_at (datetime): Date de création du profil
    """
    id: int
    user_id: int
    name: str
    email: str
    department: str
    position: str
    vacation_balance: int = 20  # Solde par défaut: 20 jours
    vacation_used: int = 0
    hire_date: datetime = None
    created_at: datetime = None

    def __post_init__(self):
        if self.hire_date is None:
            self.hire_date = datetime.now()
        if self.created_at is None:
            self.created_at = datetime.now()

    def get_vacation_available(self) -> int:
        """Retourne le nombre de jours de congés disponibles."""
        return self.vacation_balance - self.vacation_used

    def has_enough_balance(self, days_requested: int) -> bool:
        """Vérifie si l'employé a assez de congés."""
        return self.get_vacation_available() >= days_requested

    def use_vacation_days(self, days: int) -> bool:
        """Utilise des jours de congés."""
        if self.has_enough_balance(days):
            self.vacation_used += days
            return True
        return False

    def refund_vacation_days(self, days: int):
        """Rembourse des jours de congés (en cas d'annulation)."""
        self.vacation_used = max(0, self.vacation_used - days)

    def to_dict(self) -> Dict:
        """Convertit l'employé en dictionnaire."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'position': self.position,
            'vacation_balance': self.vacation_balance,
            'vacation_used': self.vacation_used,
            'vacation_available': self.get_vacation_available(),
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Employee':
        """Crée un employé à partir d'un dictionnaire."""
        return Employee(
            id=data.get('id'),
            user_id=data.get('user_id'),
            name=data.get('name'),
            email=data.get('email'),
            department=data.get('department'),
            position=data.get('position'),
            vacation_balance=data.get('vacation_balance', 20),
            vacation_used=data.get('vacation_used', 0),
            hire_date=datetime.fromisoformat(data['hire_date']) if data.get('hire_date') else None,
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
