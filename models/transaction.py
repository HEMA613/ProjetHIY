from datetime import datetime

class Transaction:
    def __init__(self, transaction_id, account, amount, transaction_type, description=''):
        self.transaction_id = transaction_id
        self.account = account
        self.amount = amount
        self.transaction_type = transaction_type  # 'deposit', 'withdraw', 'transfer'
        self.description = description
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'account_id': self.account.account_id,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data, account):
        tx = cls(data['transaction_id'], account, data['amount'], data['transaction_type'], data['description'])
        tx.timestamp = datetime.fromisoformat(data['timestamp'])
        return tx

    def calculate_duration(self):
        # Example: duration since creation, but perhaps not needed
        return (datetime.now() - self.timestamp).total_seconds()