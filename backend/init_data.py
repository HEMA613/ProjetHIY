from admin import Admin
from utilisateur import Utilisateur

print("🚀 Initialisation des données...")

# ------------------------------------------------------------------ #
#  Création des admins                                                 #
# ------------------------------------------------------------------ #

admins = [
    Admin(id=1, name="Administrateur", email="admin@gmail.com", password="admin123"),
]

for admin in admins:
    admin.sauvegarder()
    print(f"✅ Admin créé : {admin.name} | email: {admin.email} | password: {admin.password}")

# ------------------------------------------------------------------ #
#  Création des employés                                               #
# ------------------------------------------------------------------ #

employes = [
    Utilisateur(id=1, name="Jean Dupont",   email="jean@gmail.com",   password="jean123",   vacation_balance=25),
    Utilisateur(id=2, name="Marie Martin",  email="marie@gmail.com",  password="marie123",  vacation_balance=20),
    Utilisateur(id=3, name="Paul Bernard",  email="paul@gmail.com",   password="paul123",   vacation_balance=15),
]

for emp in employes:
    emp.sauvegarder()
    print(f"✅ Employé créé : {emp.name} | email: {emp.email} | password: {emp.password} | solde: {emp.vacation_balance}j")

print("\n🎉 Initialisation terminée !")
print("📁 Fichiers générés : data/admins.json | data/employes.json")
print("\n--- IDENTIFIANTS ---")
print("👑 Admin    : admin@gmail.com  / admin123")
print("👤 Employé 1: jean@gmail.com   / jean123")
print("👤 Employé 2: marie@gmail.com  / marie123")
