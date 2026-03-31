import hashlib
import sqlite3
from datetime import datetime

class User:
    def __init__(self, username, password, email=None, role='user'):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.email = email
        self.role = role  # 'user' or 'admin'
        self.created_at = datetime.now()
        self.accounts = []  # List of associated accounts

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == self._hash_password(password)

    def is_admin(self):
        return self.role == 'admin'

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'accounts': [acc.to_dict() for acc in self.accounts]
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data['username'], '', data.get('email'), data.get('role', 'user'))
        user.password_hash = data.get('password_hash', '')
        user.created_at = datetime.fromisoformat(data['created_at'])
        # accounts would be loaded separately
        return user