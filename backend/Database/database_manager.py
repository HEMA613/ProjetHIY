"""
Module Database: Gestion de la base de données SQLite
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Dict
from Models import User, Employee, VacationRequest, VacationStatus


class DatabaseManager:
    """
    Gestionnaire de base de données SQLite pour l'application.
    Gère les opérations CRUD pour tous les modèles.
    """

    def __init__(self, db_path: str = "vacation_manager.db"):
        """
        Initialise le gestionnaire de base de données.
        
        Args:
            db_path: Chemin vers le fichier de base de données
        """
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Retourne une connexion à la base de données."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialise la base de données avec les tables."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Créer la table users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'employee')),
                created_at TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1
            )
        ''')

        # Créer la table employees
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                department TEXT,
                position TEXT,
                vacation_balance INTEGER DEFAULT 20,
                vacation_used INTEGER DEFAULT 0,
                hire_date TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        # Créer la table vacation_requests
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacation_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED')),
                days_count INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                approved_by INTEGER,
                rejection_reason TEXT,
                FOREIGN KEY(employee_id) REFERENCES employees(id),
                FOREIGN KEY(approved_by) REFERENCES users(id)
            )
        ''')

        conn.commit()
        conn.close()

        # Insérer les utilisateurs par défaut
        self.insert_default_users()

    def insert_default_users(self):
        """Insère l'admin et l'employé par défaut si la table est vide."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            # Admin par défaut
            cursor.execute('''
                INSERT INTO users (username, email, password, role, created_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('admin', 'admin@company.com', 'Azerty1234', 'admin', datetime.now().isoformat(), True))

            admin_id = cursor.lastrowid

            # Employé par défaut
            cursor.execute('''
                INSERT INTO users (username, email, password, role, created_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('user', 'user@company.com', 'Azerty1234', 'employee', datetime.now().isoformat(), True))

            user_id = cursor.lastrowid

            # Profil employé
            cursor.execute('''
                INSERT INTO employees (user_id, name, email, department, position, vacation_balance, hire_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, 'Jean Dupont', 'jean.dupont@company.com', 'IT', 'Développeur', 20, datetime.now().isoformat(), datetime.now().isoformat()))

            conn.commit()

        conn.close()

    # ==================== USERS ====================

    def create_user(self, username: str, email: str, password: str, role: str) -> Optional[User]:
        """Crée un nouvel utilisateur."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password, role, created_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, password, role, datetime.now().isoformat(), True))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return self.get_user_by_id(user_id)
        except sqlite3.IntegrityError:
            return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Récupère un utilisateur par ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                password=row['password'],
                role=row['role'],
                created_at=datetime.fromisoformat(row['created_at']),
                is_active=bool(row['is_active'])
            )
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Récupère un utilisateur par email."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                password=row['password'],
                role=row['role'],
                created_at=datetime.fromisoformat(row['created_at']),
                is_active=bool(row['is_active'])
            )
        return None

    def get_all_users(self) -> List[User]:
        """Récupère tous les utilisateurs."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        conn.close()
        return [
            User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                password=row['password'],
                role=row['role'],
                created_at=datetime.fromisoformat(row['created_at']),
                is_active=bool(row['is_active'])
            )
            for row in rows
        ]

    # ==================== EMPLOYEES ====================

    def create_employee(self, user_id: int, name: str, email: str, department: str, position: str) -> Optional[Employee]:
        """Crée un profil employé."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO employees (user_id, name, email, department, position, vacation_balance, hire_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, name, email, department, position, 20, datetime.now().isoformat(), datetime.now().isoformat()))
            conn.commit()
            employee_id = cursor.lastrowid
            conn.close()
            return self.get_employee_by_id(employee_id)
        except sqlite3.IntegrityError:
            return None

    def get_employee_by_id(self, employee_id: int) -> Optional[Employee]:
        """Récupère un employé par ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Employee(
                id=row['id'],
                user_id=row['user_id'],
                name=row['name'],
                email=row['email'],
                department=row['department'],
                position=row['position'],
                vacation_balance=row['vacation_balance'],
                vacation_used=row['vacation_used'],
                hire_date=datetime.fromisoformat(row['hire_date']),
                created_at=datetime.fromisoformat(row['created_at'])
            )
        return None

    def get_employee_by_user_id(self, user_id: int) -> Optional[Employee]:
        """Récupère un employé par ID utilisateur."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Employee(
                id=row['id'],
                user_id=row['user_id'],
                name=row['name'],
                email=row['email'],
                department=row['department'],
                position=row['position'],
                vacation_balance=row['vacation_balance'],
                vacation_used=row['vacation_used'],
                hire_date=datetime.fromisoformat(row['hire_date']),
                created_at=datetime.fromisoformat(row['created_at'])
            )
        return None

    def get_all_employees(self) -> List[Employee]:
        """Récupère tous les employés."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees')
        rows = cursor.fetchall()
        conn.close()
        return [
            Employee(
                id=row['id'],
                user_id=row['user_id'],
                name=row['name'],
                email=row['email'],
                department=row['department'],
                position=row['position'],
                vacation_balance=row['vacation_balance'],
                vacation_used=row['vacation_used'],
                hire_date=datetime.fromisoformat(row['hire_date']),
                created_at=datetime.fromisoformat(row['created_at'])
            )
            for row in rows
        ]

    def update_employee_vacation(self, employee_id: int, vacation_used: int):
        """Met à jour les congés utilisés d'un employé."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE employees SET vacation_used = ? WHERE id = ?', (vacation_used, employee_id))
        conn.commit()
        conn.close()

    # ==================== VACATION REQUESTS ====================

    def create_vacation_request(self, vacation_request: VacationRequest) -> Optional[VacationRequest]:
        """Crée une nouvelle demande de congés."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO vacation_requests 
                (employee_id, start_date, end_date, reason, status, days_count, created_at, updated_at, approved_by, rejection_reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                vacation_request.employee_id,
                vacation_request.start_date.isoformat() if isinstance(vacation_request.start_date, datetime) else vacation_request.start_date,
                vacation_request.end_date.isoformat() if isinstance(vacation_request.end_date, datetime) else vacation_request.end_date,
                vacation_request.reason,
                vacation_request.status.value,
                vacation_request.days_count,
                vacation_request.created_at.isoformat() if vacation_request.created_at else datetime.now().isoformat(),
                vacation_request.updated_at.isoformat() if vacation_request.updated_at else datetime.now().isoformat(),
                vacation_request.approved_by,
                vacation_request.rejection_reason
            ))
            conn.commit()
            request_id = cursor.lastrowid
            conn.close()
            return self.get_vacation_request_by_id(request_id)
        except Exception as e:
            print(f"Erreur lors de la création: {e}")
            return None

    def get_vacation_request_by_id(self, request_id: int) -> Optional[VacationRequest]:
        """Récupère une demande de congés par ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vacation_requests WHERE id = ?', (request_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return VacationRequest(
                id=row['id'],
                employee_id=row['employee_id'],
                start_date=datetime.fromisoformat(row['start_date']),
                end_date=datetime.fromisoformat(row['end_date']),
                reason=row['reason'],
                status=VacationStatus(row['status']),
                days_count=row['days_count'],
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at']),
                approved_by=row['approved_by'],
                rejection_reason=row['rejection_reason']
            )
        return None

    def get_vacation_requests_by_employee(self, employee_id: int) -> List[VacationRequest]:
        """Récupère toutes les demandes d'un employé."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vacation_requests WHERE employee_id = ? ORDER BY created_at DESC', (employee_id,))
        rows = cursor.fetchall()
        conn.close()
        return [
            VacationRequest(
                id=row['id'],
                employee_id=row['employee_id'],
                start_date=datetime.fromisoformat(row['start_date']),
                end_date=datetime.fromisoformat(row['end_date']),
                reason=row['reason'],
                status=VacationStatus(row['status']),
                days_count=row['days_count'],
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at']),
                approved_by=row['approved_by'],
                rejection_reason=row['rejection_reason']
            )
            for row in rows
        ]

    def get_all_pending_vacation_requests(self) -> List[VacationRequest]:
        """Récupère toutes les demandes en attente."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM vacation_requests 
            WHERE status = 'PENDING' 
            ORDER BY created_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [
            VacationRequest(
                id=row['id'],
                employee_id=row['employee_id'],
                start_date=datetime.fromisoformat(row['start_date']),
                end_date=datetime.fromisoformat(row['end_date']),
                reason=row['reason'],
                status=VacationStatus(row['status']),
                days_count=row['days_count'],
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at']),
                approved_by=row['approved_by'],
                rejection_reason=row['rejection_reason']
            )
            for row in rows
        ]

    def get_all_vacation_requests(self) -> List[VacationRequest]:
        """Récupère toutes les demandes de congés."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vacation_requests ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [
            VacationRequest(
                id=row['id'],
                employee_id=row['employee_id'],
                start_date=datetime.fromisoformat(row['start_date']),
                end_date=datetime.fromisoformat(row['end_date']),
                reason=row['reason'],
                status=VacationStatus(row['status']),
                days_count=row['days_count'],
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at']),
                approved_by=row['approved_by'],
                rejection_reason=row['rejection_reason']
            )
            for row in rows
        ]

    def update_vacation_request_status(self, request_id: int, status: VacationStatus, approved_by: int = None, rejection_reason: str = None):
        """Met à jour le statut d'une demande de congés."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE vacation_requests 
            SET status = ?, updated_at = ?, approved_by = ?, rejection_reason = ?
            WHERE id = ?
        ''', (status.value, datetime.now().isoformat(), approved_by, rejection_reason, request_id))
        conn.commit()
        conn.close()
