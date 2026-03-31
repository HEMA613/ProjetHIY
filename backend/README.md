# Backend - Vacation Manager System

## 📋 Description
Le backend est responsable de toute la logique métier, la gestion des données et l'architecture du système de gestion des congés.

## 🏗️ Architecture

### Structure des dossiers
```
backend/
├── Models/              # Classes de données
│   ├── user.py         # Modèle utilisateur
│   ├── employee.py     # Modèle employé
│   ├── vacation_request.py  # Modèle demandes de congés
│   └── __init__.py
├── Database/           # Gestion de la base de données
│   ├── database_manager.py  # Gestionnaire SQLite
│   └── __init__.py
├── Services/           # Logique métier
│   ├── auth_service.py      # Service d'authentification
│   ├── employee_service.py  # Service gestion employés
│   ├── vacation_service.py  # Service gestion congés
│   └── __init__.py
├── app.py             # Application principale
├── requirements.txt   # Dépendances
└── README.md         # Cette documentation
```

## 📦 Modèles de données

### User (Utilisateur)
Gère l'authentification et les rôles.
```python
- id: int
- username: str
- email: str
- password: str
- role: str ('admin' ou 'employee')
- created_at: datetime
- is_active: bool
```

### Employee (Employé)
Gère les profils et soldes de congés.
```python
- id: int
- user_id: int
- name: str
- email: str
- department: str
- position: str
- vacation_balance: int (20 jours par défaut)
- vacation_used: int
- hire_date: datetime
- created_at: datetime
```

**Méthodes utiles:**
- `get_vacation_available()`: Retourne les jours disponibles
- `has_enough_balance(days)`: Vérifie la disponibilité
- `use_vacation_days(days)`: Utilise des jours
- `refund_vacation_days(days)`: Rembourse des jours

### VacationRequest (Demande de congés)
Gère les demandes et leur cycle de vie.
```python
- id: int
- employee_id: int
- start_date: datetime
- end_date: datetime
- reason: str
- status: VacationStatus (PENDING/APPROVED/REJECTED/CANCELLED)
- days_count: int
- created_at: datetime
- updated_at: datetime
- approved_by: int (optionnel)
- rejection_reason: str (optionnel)
```

**Statuts:**
- `PENDING`: En attente d'approbation
- `APPROVED`: Approuvée
- `REJECTED`: Rejetée
- `CANCELLED`: Annulée

**Méthodes utiles:**
- `calculate_days()`: Calcule le nombre de jours
- `is_valid()`: Valide les dates
- `approve(admin_id)`: Approuve la demande
- `reject(reason)`: Rejette la demande

## 🔧 Services

### AuthService
Service d'authentification et gestion des utilisateurs.

```python
from Services import AuthService
from Database import DatabaseManager

db = DatabaseManager()
auth = AuthService(db)

# Authentification
user = auth.authenticate('email@company.com', 'password')

# Créer un utilisateur
new_user = auth.create_user('username', 'email@company.com', 'password', 'employee')

# Vérifier le rôle
is_admin = auth.is_admin(user_id)
```

### EmployeeService
Service de gestion des employés.

```python
from Services import EmployeeService

employee_service = EmployeeService(db)

# Récupérer un employé
employee = employee_service.get_employee(employee_id)

# Vérifier le solde
balance = employee_service.get_vacation_balance(employee_id)

# Obtenir les détails
details = employee_service.get_vacation_details(employee_id)
# Retourne: {'total_balance': 20, 'days_used': 5, 'days_available': 15}

# Utiliser des jours
success = employee_service.use_vacation_days(employee_id, 3)

# Rembourser des jours
success = employee_service.refund_vacation_days(employee_id, 3)
```

### VacationService
Service de gestion des demandes de congés.

```python
from Services import VacationService
from datetime import datetime, timedelta

vacation_service = VacationService(db)

# Soumettre une demande
start = datetime.now() + timedelta(days=5)
end = datetime.now() + timedelta(days=7)
request = vacation_service.submit_vacation_request(
    employee_id=1,
    start_date=start,
    end_date=end,
    reason="Vacances d'été"
)

# Récupérer les demandes
pending = vacation_service.get_pending_vacation_requests()
requests = vacation_service.get_employee_vacation_requests(employee_id)

# Approuver une demande
approved = vacation_service.approve_vacation_request(request_id, admin_id)

# Rejeter une demande
rejected = vacation_service.reject_vacation_request(request_id, "Conflits de calendrier")

# Annuler une demande
cancelled = vacation_service.cancel_vacation_request(request_id)

# Statistiques
stats = vacation_service.get_employee_vacation_statistics(employee_id)
# Retourne: 
# {
#     'total_balance': 20,
#     'used_days': 5,
#     'available_days': 15,
#     'pending_requests': 2,
#     'pending_days': 6,
#     'approved_requests': 1,
#     'rejected_requests': 0,
#     'total_requests': 3
# }
```

## 💾 Base de données

Le système utilise **SQLite** pour la persistance des données.

### Initialisaton automatique

Lors du premier lancement, le `DatabaseManager` crée automatiquement:
- Les tables (users, employees, vacation_requests)
- Un utilisateur admin: `admin@company.com` / `Azerty1234`
- Un utilisateur employé: `user@company.com` / `Azerty1234`

### Fichier de base de données
- **Chemin**: `vacation_manager.db`
- **Localisation**: Au même niveau que `app.py`

## 🔐 Sécurité et Cohérence

Le système garantit la cohérence des données:
- ✓ Validation des dates (pas dans le passé)
- ✓ Vérification du solde de congés
- ✓ Calcul automatique des jours
- ✓ Gestion des statuts cohérents
- ✓ Audit (created_at, updated_at, approved_by)

## 🚀 Utilisation

### Lancer les tests
```bash
cd backend
python app.py
```

### Importer dans votre application
```python
from Models import User, Employee, VacationRequest
from Database import DatabaseManager
from Services import AuthService, EmployeeService, VacationService

# Initialiser
db = DatabaseManager()
auth = AuthService(db)
employees = EmployeeService(db)
vacations = VacationService(db)
```

## 📚 Exemple complet

```python
from Services import AuthService, EmployeeService, VacationService
from Database import DatabaseManager
from datetime import datetime, timedelta

# Initialiser les services
db = DatabaseManager()
auth = AuthService(db)
emp_service = EmployeeService(db)
vac_service = VacationService(db)

# 1. Authentification
user = auth.authenticate('user@company.com', 'Azerty1234')
if user:
    print(f"Connecté: {user.username}")

    # 2. Récupérer l'employé
    employee = emp_service.get_employee_by_user_id(user.id)
    print(f"Solde: {employee.get_vacation_available()} jours")

    # 3. Soumettre une demande
    start = datetime.now() + timedelta(days=10)
    end = datetime.now() + timedelta(days=12)
    request = vac_service.submit_vacation_request(
        employee.id, start, end, "Vacances"
    )
    print(f"Demande #{request.id} créée")

    # 4. Voir les statistiques
    stats = vac_service.get_employee_vacation_statistics(employee.id)
    print(f"Jours disponibles: {stats['available_days']}")
```

## 🎯 Compétences mises en avant

- **Architecture logicielle**: Séparation des responsabilités (Models/Services/Database)
- **POO**: Utilisation des classes, héritage et encapsulation
- **Gestion des données**: Validation, cohérence, audit
- **Base de données**: SQLite, requêtes optimisées, schéma bien structuré

## 📝 Notes

- Pas de dépendances externes (utilise la stdlib Python)
- Support complet des dates et fuseaux horaires
- Transactions ACID garanties
- Extensible facilement pour ajouter des fonctionnalités
