"""
Module User: Gestion des utilisateurs et authentification
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass
class User:
    """
    Classe représentant un utilisateur du système.
    Attributs:
        id (int): Identifiant unique
        username (str): Nom d'utilisateur
        email (str): Adresse email
        password (str): Mot de passe (hashé)
        role (str): Rôle - 'admin' ou 'employee'
        created_at (datetime): Date de création
        is_active (bool): Statut du compte
    """
    id: int
    username: str
    email: str
    password: str
    role: str  # 'admin' ou 'employee'
    created_at: datetime = None
    is_active: bool = True

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self) -> Dict:
        """Convertit l'utilisateur en dictionnaire."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

    @staticmethod
    def from_dict(data: Dict) -> 'User':
        """Crée un utilisateur à partir d'un dictionnaire."""
        return User(
            id=data.get('id'),
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            role=data.get('role'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            is_active=data.get('is_active', True)
        )
