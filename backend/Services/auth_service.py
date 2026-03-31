"""
Module AuthService: Service d'authentification
"""
from typing import Optional
from Models import User
from Database import DatabaseManager


class AuthService:
    """
    Service d'authentification pour l'application.
    Gère la connexion, la création de comptes et la gestion des utilisateurs.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialise le service d'authentification.
        
        Args:
            db_manager: Instance du gestionnaire de base de données
        """
        self.db = db_manager

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Authentifie un utilisateur avec email et mot de passe.
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe de l'utilisateur
            
        Returns:
            L'utilisateur s'il est authentifié, None sinon
        """
        user = self.db.get_user_by_email(email)
        if user and user.is_active and user.password == password:
            return user
        return None

    def create_user(self, username: str, email: str, password: str, role: str = 'employee') -> Optional[User]:
        """
        Crée un nouvel utilisateur.
        
        Args:
            username: Nom d'utilisateur unique
            email: Email unique
            password: Mot de passe
            role: Rôle ('admin' ou 'employee')
            
        Returns:
            L'utilisateur créé ou None si échec
        """
        if role not in ['admin', 'employee']:
            return None
        
        return self.db.create_user(username, email, password, role)

    def get_user(self, user_id: int) -> Optional[User]:
        """Récupère un utilisateur par ID."""
        return self.db.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Récupère un utilisateur par email."""
        return self.db.get_user_by_email(email)

    def get_all_users(self) -> list:
        """Récupère tous les utilisateurs."""
        return self.db.get_all_users()

    def is_admin(self, user_id: int) -> bool:
        """Vérifie si l'utilisateur est administrateur."""
        user = self.db.get_user_by_id(user_id)
        return user and user.role == 'admin'

    def is_employee(self, user_id: int) -> bool:
        """Vérifie si l'utilisateur est employé."""
        user = self.db.get_user_by_id(user_id)
        return user and user.role == 'employee'
