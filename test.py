#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models import User, Account, Transaction, Storage

def main():
    # Initialize storage
    storage = Storage()

    # Create an admin user
    admin = User("admin", "azerty1234", "admin@example.com", "admin")
    print(f"Created admin: {admin.username}, role: {admin.role}")

    # Save admin
    storage.save_user(admin)
    print("Admin saved to database")

    # Create a regular user
    user = User("testuser", "azerty123", "test@example.com", "user")
    print(f"Created user: {user.username}, role: {user.role}")

    # Save user
    storage.save_user(user)
    print("User saved to database")

    # Create an account for the user (start with 0, add initial deposit)
    account = Account("acc001", user, 0.0, "active")
    user.accounts.append(account)
    print(f"Created account with balance: {account.balance}")

    # Initial deposit
    initial_tx = Transaction("tx000", account, 1000.0, "deposit", "Initial deposit")
    account.transactions.append(initial_tx)
    storage.save_transaction(initial_tx)
    print("Initial deposit saved")

    # Save account
    storage.save_account(account)
    print("Account saved to database")

    # Perform a transaction
    transaction = Transaction("tx001", account, 200.0, "withdraw", "Test withdrawal")
    account.transactions.append(transaction)
    print(f"Created transaction: {transaction.transaction_type} {transaction.amount}")

    # Save transaction (this will update balance)
    storage.save_transaction(transaction)
    print("Transaction saved, balance updated")

    # Load user from database
    loaded_user = storage.load_user("testuser")
    if loaded_user:
        print(f"Loaded user: {loaded_user.username}")
        print(f"User has {len(loaded_user.accounts)} account(s)")
        for acc in loaded_user.accounts:
            print(f"Account {acc.account_id}: Balance {acc.balance}, Status {acc.status}")
            print(f"Transactions: {len(acc.transactions)}")
            for tx in acc.transactions:
                print(f"  TX {tx.transaction_id}: {tx.transaction_type} {tx.amount} at {tx.timestamp}")

    # Test admin controls
    if admin.is_admin():
        print("Admin has admin privileges")
        all_users = storage.get_all_users()
        print(f"Admin sees {len(all_users)} users")
        for u in all_users:
            print(f"  - {u.username} ({u.role})")
    else:
        print("Admin check failed")

    # Test password check
    if user.check_password("azerty123"):
        print("User password check: OK")
    else:
        print("User password check: Failed")

    if admin.check_password("azerty1234"):
        print("Admin password check: OK")
    else:
        print("Admin password check: Failed")

if __name__ == "__main__":
    main()