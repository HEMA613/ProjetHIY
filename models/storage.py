import sqlite3
import json
from datetime import datetime
from .user import User
from .account import Account
from .transaction import Transaction

class Storage:
    def __init__(self, db_path='data/miy.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT,
                    email TEXT,
                    role TEXT DEFAULT 'user',
                    created_at TEXT
                )
            ''')
            # Accounts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id TEXT PRIMARY KEY,
                    username TEXT,
                    balance REAL,
                    status TEXT,
                    created_at TEXT,
                    FOREIGN KEY (username) REFERENCES users (username)
                )
            ''')
            # Transactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    account_id TEXT,
                    amount REAL,
                    transaction_type TEXT,
                    description TEXT,
                    timestamp TEXT,
                    FOREIGN KEY (account_id) REFERENCES accounts (account_id)
                )
            ''')
            conn.commit()

    def save_user(self, user):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (username, password_hash, email, role, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user.username, user.password_hash, user.email, user.role, user.created_at.isoformat()))
            conn.commit()

    def load_user(self, username):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            if row:
                user = User(row[0], '', row[2], row[3])  # username, password, email, role
                user.password_hash = row[1]
                user.created_at = datetime.fromisoformat(row[4])
                # Load accounts
                user.accounts = self.load_accounts_for_user(username)
                for acc in user.accounts:
                    acc.user = user
                    for tx in acc.transactions:
                        tx.account = acc
                return user
        return None

    def save_account(self, account):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO accounts (account_id, username, balance, status, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (account.account_id, account.user.username, account.balance, account.status, account.created_at.isoformat()))
            conn.commit()

    def load_accounts_for_user(self, username):
        accounts = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM accounts WHERE username = ?', (username,))
            for row in cursor.fetchall():
                account = Account(row[0], None, row[2], row[3])  # user set later
                account.created_at = datetime.fromisoformat(row[4])
                account.transactions = self.load_transactions_for_account(row[0])
                accounts.append(account)
        return accounts

    def save_transaction(self, transaction):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO transactions (transaction_id, account_id, amount, transaction_type, description, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (transaction.transaction_id, transaction.account.account_id, transaction.amount, transaction.transaction_type, transaction.description, transaction.timestamp.isoformat()))
            conn.commit()
        # Update balance for consistency
        self.update_balance(transaction.account.account_id)

    def load_transactions_for_account(self, account_id):
        transactions = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM transactions WHERE account_id = ?', (account_id,))
            for row in cursor.fetchall():
                tx = Transaction(row[0], None, row[2], row[3], row[4])  # account set later
                tx.timestamp = datetime.fromisoformat(row[5])
                transactions.append(tx)
        return transactions

    # For data consistency, methods to update balance based on transactions
    def get_all_users(self):
        users = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT username FROM users')
            usernames = [row[0] for row in cursor.fetchall()]
            for username in usernames:
                user = self.load_user(username)
                if user:
                    users.append(user)
        return users

    def delete_user(self, username):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Delete transactions
            cursor.execute('DELETE FROM transactions WHERE account_id IN (SELECT account_id FROM accounts WHERE username = ?)', (username,))
            # Delete accounts
            cursor.execute('DELETE FROM accounts WHERE username = ?', (username,))
            # Delete user
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()

    def update_balance(self, account_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT SUM(CASE WHEN transaction_type = 'deposit' THEN amount ELSE -amount END)
                FROM transactions WHERE account_id = ?
            ''', (account_id,))
            balance = cursor.fetchone()[0] or 0
            cursor.execute('UPDATE accounts SET balance = ? WHERE account_id = ?', (balance, account_id))
            conn.commit()