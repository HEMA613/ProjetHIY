import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date
from manager import Manager
from Utilisateur import Employee
from gestionnaire import Gestionnaire
import json, pathlib

OK  = "\033[92m✅"
RST = "\033[0m"
SEP = "─" * 50

def titre(t):
    print(f"\n{SEP}\n🔹 {t}\n{SEP}")

# 0. NETTOYAGE
titre("0. Nettoyage des fichiers JSON")
pathlib.Path("data").mkdir(exist_ok=True)
for f in ["data/manager.json", "data/employes.json", "data/demandes.json"]:
    with open(f, "w") as fp:
        json.dump([], fp)
print(f"{OK} Fichiers JSON réinitialisés{RST}")

# 1. CRÉATION
titre("1. Création des comptes")
admin = Manager(id=1, name="Administrateur", email="admin@gmail.com", password="admin123")
admin.sauvegarder()
print(f"{OK} Manager créé : {admin}{RST}")

jean  = Employee(id=1, name="Jean Dupont",  email="jean@gmail.com",  password="jean123",  vacation_balance=25)
marie = Employee(id=2, name="Marie Martin", email="marie@gmail.com", password="marie123", vacation_balance=10)
jean.sauvegarder()
marie.sauvegarder()
print(f"{OK} Jean créé  : {jean}{RST}")
print(f"{OK} Marie créée: {marie}{RST}")

# 2. LOGIN
titre("2. Test Login")
session_admin = Gestionnaire.login("admin@gmail.com", "admin123")
assert session_admin and session_admin["role"] == "manager"
print(f"{OK} Login manager OK → rôle: {session_admin['role']}{RST}")

session_jean = Gestionnaire.login("jean@gmail.com", "jean123")
assert session_jean and session_jean["role"] == "employee"
print(f"{OK} Login jean OK  → rôle: {session_jean['role']}{RST}")

session_fail = Gestionnaire.login("hacker@gmail.com", "wrong")
assert session_fail is None
print(f"{OK} Login invalide rejeté{RST}")

# 3. SOUMETTRE
titre("3. Soumission de demandes")
user_jean = session_jean["user"]

d1 = Gestionnaire.soumettre_demande(user_jean, date(2025, 7, 1), date(2025, 7, 5), "Vacances")
assert d1 is not None and d1["days"] == 5
print(f"{OK} Demande 1 : {d1['days']}j du {d1['start_date']} au {d1['end_date']}{RST}")

d2 = Gestionnaire.soumettre_demande(user_jean, date(2025, 8, 10), date(2025, 8, 12), "Famille")
assert d2 is not None
print(f"{OK} Demande 2 : {d2['days']}j{RST}")

d_bad = Gestionnaire.soumettre_demande(user_jean, date(2025, 9, 10), date(2025, 9, 5), "Erreur")
assert d_bad is None
print(f"{OK} Dates invalides rejetées{RST}")

session_marie = Gestionnaire.login("marie@gmail.com", "marie123")
user_marie = session_marie["user"]
d_insuf = Gestionnaire.soumettre_demande(user_marie, date(2025, 6, 1), date(2025, 6, 15), "Trop long")
assert d_insuf is None
print(f"{OK} Solde insuffisant rejeté{RST}")

# 4. MANAGER : demandes en attente
titre("4. Manager — demandes en attente")
admin_user = session_admin["user"]
en_attente = admin_user.voir_demandes_en_attente()
assert len(en_attente) == 2
print(f"{OK} {len(en_attente)} demande(s) en attente{RST}")
for d in en_attente:
    print(f"   → ID {d['id']} | {d['employee_name']} | {d['days']}j | {d['status']}")

# 5. APPROUVER
titre("5. Manager — approuver demande ID 1")
resultat = Gestionnaire.approuver_demande(admin_user, demande_id=1)
assert resultat is True
print(f"{OK} Demande 1 approuvée{RST}")
jean_maj = Employee.trouver_par_id(1)
assert jean_maj.vacation_balance == 20
print(f"{OK} Solde Jean : {jean_maj.vacation_balance}j restants{RST}")

# 6. REFUSER
titre("6. Manager — refuser demande ID 2")
resultat = Gestionnaire.refuser_demande(admin_user, demande_id=2, motif="Période chargée")
assert resultat is True
print(f"{OK} Demande 2 refusée{RST}")

# 7. MES DEMANDES
titre("7. Jean — voir ses demandes")
mes_dem = Gestionnaire.mes_demandes(user_jean)
assert len(mes_dem) == 2
print(f"{OK} Jean a {len(mes_dem)} demande(s){RST}")
for d in mes_dem:
    print(f"   → ID {d['id']} | {d['days']}j | {d['status']}")

# 8. STATS
titre("8. Statistiques")
stats = Gestionnaire.statistiques()
assert stats["total_demandes"] == 2
assert stats["approuvees"] == 1
assert stats["refusees"] == 1
print(f"{OK} Stats OK : {stats}{RST}")

# 9. ANNULER
titre("9. Annuler une demande")
d3 = Gestionnaire.soumettre_demande(user_jean, date(2025, 10, 1), date(2025, 10, 3), "A annuler")
assert d3 is not None
annulation = Gestionnaire.annuler_demande(user_jean, d3["id"])
assert annulation is True
print(f"{OK} Demande annulée{RST}")

# RÉSULTAT
print(f"\n{'═' * 50}")
print(f"\033[92m🎉 TOUS LES TESTS PASSÉS ! Backend opérationnel.\033[0m")
print(f"{'═' * 50}\n")