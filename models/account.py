from datetime import datetime

class Account:
    def __init__(self, account_id, user, balance=0.0, status='active'):
        self.account_id = account_id
        self.user = user
        self.balance = balance
        self.status = status  # 'active', 'frozen', etc.
        self.created_at = datetime.now()
        self.transactions = []  # List of transactions

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'user_username': self.user.username,
            'balance': self.balance,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'transactions': [tx.to_dict() for tx in self.transactions]
        }

    @classmethod
    def from_dict(cls, data, user):
        account = cls(data['account_id'], user, data['balance'], data['status'])
        account.created_at = datetime.fromisoformat(data['created_at'])
        # transactions loaded separately
        return account