from .manager import Manager
from .Utilisateur import Employee

print("🚀 Initialisation des données...")

# ------------------------------------------------------------------ #
#  Création des managers                                                 #
# ------------------------------------------------------------------ #

managers = [
    Manager(id=1, name="Manager", email="manager@gmail.com", password="manager123"),
]

for manager in managers:
    manager.sauvegarder()
    print(f"✅ Manager créé : {manager.name} | email: {manager.email} | password: {manager.password}")

# ------------------------------------------------------------------ #
#  Création des employés                                               #
# ------------------------------------------------------------------ #

employes = [
    Employee(id=1, name="Jean Dupont",   email="jean@gmail.com",   password="jean123",   vacation_balance=25),
    Employee(id=2, name="Marie Martin",  email="marie@gmail.com",  password="marie123",  vacation_balance=20),
    Employee(id=3, name="Paul Bernard",  email="paul@gmail.com",   password="paul123",   vacation_balance=15),
]

for emp in employes:
    emp.sauvegarder()
    print(f"✅ Employee créé : {emp.name} | email: {emp.email} | password: {emp.password} | solde: {emp.vacation_balance}j")

print("\n🎉 Initialisation terminée !")
print("📁 Fichiers générés : data/manager.json | data/employes.json")
print("\n--- IDENTIFIANTS ---")
print("👑 Manager  : manager@gmail.com  / manager123")
print("👤 Employee 1: jean@gmail.com   / jean123")
print("👤 Employee 2: marie@gmail.com  / marie123")
print("👤 Employee 3: paul@gmail.com   / paul123")