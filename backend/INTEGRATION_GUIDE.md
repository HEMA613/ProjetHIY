# 🔌 Guide d'Intégration Backend - API & Services

Ce document explique comment intégrer le backend avec le frontend.

## 📡 Étape 1: Initialiser les Services

```python
from Services import AuthService, EmployeeService, VacationService
from Database import DatabaseManager

# Initialiser une seule fois au démarrage
db = DatabaseManager("vacation_manager.db")
auth_service = AuthService(db)
employee_service = EmployeeService(db)
vacation_service = VacationService(db)
```

## 🔐 Authentification

### Login
```python
def login(email: str, password: str):
    user = auth_service.authenticate(email, password)
    if user:
        return {
            'success': True,
            'user_id': user.id,
            'role': user.role,
            'username': user.username
        }
    return {'success': False, 'error': 'Identifiants invalides'}

# Exemple:
# login('admin@company.com', 'Azerty1234')
# login('user@company.com', 'Azerty1234')
```

### Créer un Utilisateur (Admin uniquement)
```python
def create_new_user(email: str, username: str, password: str, role: str):
    user = auth_service.create_user(username, email, password, role)
    if user:
        return {'success': True, 'user_id': user.id}
    return {'success': False, 'error': 'Email ou username déjà utilisé'}
```

### Vérifier un Rôle
```python
def check_role(user_id: int):
    if auth_service.is_admin(user_id):
        return 'admin'
    elif auth_service.is_employee(user_id):
        return 'employee'
    return None
```

---

## 👥 Gestion des Employés

### Dashboard Employé - Récupérer les Informations
```python
def get_employee_dashboard(user_id: int):
    employee = employee_service.get_employee_by_user_id(user_id)
    if employee:
        stats = vacation_service.get_employee_vacation_statistics(employee.id)
        return {
            'name': employee.name,
            'position': employee.position,
            'department': employee.department,
            'vacation_balance': stats['total_balance'],
            'vacation_used': stats['used_days'],
            'vacation_available': stats['available_days'],
            'pending_requests': stats['pending_requests'],
            'pending_days': stats['pending_days'],
            'approved_requests': stats['approved_requests'],
            'total_requests': stats['total_requests']
        }
    return None
```

### Récupérer les Infos Complètes d'un Employé
```python
def get_employee_full_info(user_id: int):
    return employee_service.get_employee_info(employee_service.get_employee_by_user_id(user_id).id)
    # Retourne:
    # {
    #     'id': 1,
    #     'user_id': 1,
    #     'name': 'Jean Dupont',
    #     'email': 'jean.dupont@company.com',
    #     'department': 'IT',
    #     'position': 'Développeur',
    #     'username': 'user',
    #     'vacation_balance': 20,
    #     'vacation_used': 5,
    #     'vacation_available': 15,
    #     'hire_date': '2024-01-15T10:30:00'
    # }
```

### Liste Tous les Employés (Admin)
```python
def get_all_employees():
    employees = employee_service.get_all_employees()
    return [
        {
            'id': emp.id,
            'name': emp.name,
            'department': emp.department,
            'position': emp.position,
            'vacation_available': emp.get_vacation_available(),
            'vacation_used': emp.vacation_used
        }
        for emp in employees
    ]
```

---

## 🏖️ Gestion des Demandes de Congés

### Soumettre une Demande (Employé)
```python
from datetime import datetime, timedelta

def submit_vacation_request(user_id: int, start_date_str: str, end_date_str: str, reason: str):
    employee = employee_service.get_employee_by_user_id(user_id)
    if not employee:
        return {'success': False, 'error': 'Employé non trouvé'}
    
    try:
        start = datetime.fromisoformat(start_date_str)
        end = datetime.fromisoformat(end_date_str)
        
        request = vacation_service.submit_vacation_request(
            employee.id, start, end, reason
        )
        
        if request:
            return {
                'success': True,
                'request_id': request.id,
                'days_count': request.days_count,
                'message': f'Demande de {request.days_count} jours créée'
            }
        else:
            return {
                'success': False,
                'error': 'Données invalides ou solde insuffisant'
            }
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Exemple:
# submit_vacation_request(
#     user_id=2,
#     start_date_str='2026-04-10T00:00:00',
#     end_date_str='2026-04-12T00:00:00',
#     reason='Vacances familiales'
# )
```

### Mes Demandes (Employé)
```python
def get_my_vacation_requests(user_id: int):
    employee = employee_service.get_employee_by_user_id(user_id)
    if not employee:
        return []
    
    requests = vacation_service.get_employee_vacation_requests(employee.id)
    return [
        {
            'id': req.id,
            'start_date': req.start_date.isoformat(),
            'end_date': req.end_date.isoformat(),
            'days_count': req.days_count,
            'reason': req.reason,
            'status': req.status.value,
            'created_at': req.created_at.isoformat(),
            'rejection_reason': req.rejection_reason
        }
        for req in requests
    ]
```

### Demandes en Attente (Admin)
```python
def get_pending_requests():
    requests = vacation_service.get_pending_vacation_requests()
    result = []
    
    for req in requests:
        employee = employee_service.get_employee(req.employee_id)
        result.append({
            'id': req.id,
            'employee_name': employee.name if employee else 'Inconnu',
            'employee_id': req.employee_id,
            'start_date': req.start_date.isoformat(),
            'end_date': req.end_date.isoformat(),
            'days_count': req.days_count,
            'reason': req.reason,
            'created_at': req.created_at.isoformat()
        })
    
    return result
```

### Approuver une Demande (Admin)
```python
def approve_request(request_id: int, admin_user_id: int):
    # Récupérer l'admin
    admin = auth_service.get_user(admin_user_id)
    if not admin or not auth_service.is_admin(admin_user_id):
        return {'success': False, 'error': 'Permissions insuffisantes'}
    
    success = vacation_service.approve_vacation_request(request_id, admin_user_id)
    if success:
        return {'success': True, 'message': 'Demande approuvée'}
    return {'success': False, 'error': 'Demande introuvable ou déjà traitée'}
```

### Rejeter une Demande (Admin)
```python
def reject_request(request_id: int, reason: str):
    success = vacation_service.reject_vacation_request(request_id, reason)
    if success:
        return {'success': True, 'message': 'Demande rejetée'}
    return {'success': False, 'error': 'Demande introuvable ou déjà traitée'}
```

### Annuler une Demande (Employé)
```python
def cancel_my_request(request_id: int, user_id: int):
    req = vacation_service.get_vacation_request(request_id)
    if not req:
        return {'success': False, 'error': 'Demande introuvable'}
    
    employee = employee_service.get_employee_by_user_id(user_id)
    if not employee or req.employee_id != employee.id:
        return {'success': False, 'error': 'Permissions insuffisantes'}
    
    success = vacation_service.cancel_vacation_request(request_id)
    if success:
        return {'success': True, 'message': 'Demande annulée et congés remboursés'}
    return {'success': False, 'error': 'Impossible d\'annuler cette demande'}
```

### Détails d'une Demande
```python
def get_request_details(request_id: int):
    return vacation_service.get_vacation_request_details(request_id)
    # Retourne:
    # {
    #     'id': 1,
    #     'employee': {
    #         'id': 1,
    #         'name': 'Jean Dupont',
    #         'department': 'IT'
    #     },
    #     'start_date': '2026-04-10T00:00:00',
    #     'end_date': '2026-04-12T00:00:00',
    #     'days_count': 3,
    #     'reason': 'Vacances familiales',
    #     'status': 'PENDING',
    #     'created_at': '2026-03-31T10:30:00',
    #     'updated_at': '2026-03-31T10:30:00',
    #     'approved_by': None,
    #     'rejection_reason': None
    # }
```

---

## 📊 Statistiques

### Statistiques d'un Employé
```python
def get_employee_stats(user_id: int):
    employee = employee_service.get_employee_by_user_id(user_id)
    if employee:
        return vacation_service.get_employee_vacation_statistics(employee.id)
    return None
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

---

## ⚠️ Gestion d'Erreurs Courantes

### Validation des Dates
```python
# Les dates doivent être:
# - Dans le futur
# - start_date < end_date
# - Format ISO: '2026-04-10T00:00:00'

# Erreurs possibles:
# - "Dates invalides ou solde insuffisant"
# - Si start_date >= end_date
# - Si start_date < aujourd'hui
```

### Solde de Congés
```python
# Avant d'approuver, le système vérifie:
# - L'employé a assez de jours
# - Le statut est PENDING
# - Les dates sont valides

# Si approbation: vacation_used augmente
# Si annulation: vacation_used diminue (remboursement)
```

### Permissions
```python
# Pour les admin:
# - Approuver/rejeter des demandes
# - Voir toutes les demandes
# - Voir tous les employés

# Pour les employés:
# - Voir leurs propres demandes
# - Soumettre des demandes
# - Annuler leurs demandes non approuvées
```

---

## 🔄 Flux Complet - Exemple Applicatif

```python
# 1. Utilisateur se connecte
user = auth_service.authenticate('user@company.com', 'Azerty1234')
print(f"Connecté: {user.username}, Role: {user.role}")

# 2. Récupérer les données d'affichage
if user.role == 'employee':
    dashboard = get_employee_dashboard(user.id)
    print(f"Jours disponibles: {dashboard['vacation_available']}")
    
    # 3. Soumettre une demande
    result = submit_vacation_request(
        user.id,
        '2026-04-10T00:00:00',
        '2026-04-12T00:00:00',
        'Vacances d\'été'
    )
    
    if result['success']:
        request_id = result['request_id']
        print(f"Demande #{request_id} créée pour {result['days_count']} jours")
        
        # 4. Voir mes demandes
        my_requests = get_my_vacation_requests(user.id)
        print(f"Total demandes: {len(my_requests)}")

# 5. Admin approuve la demande
if auth_service.is_admin(user.id):
    pending = get_pending_requests()
    print(f"Demandes en attente: {len(pending)}")
    
    if pending:
        request_id = pending[0]['id']
        approval = approve_request(request_id, user.id)
        print(f"Demande approuvée: {approval['message']}")
```

---

## 🎯 Résumé des Points d'Intégration

| Fonctionnalité | Service | Méthode | Retour |
|---|---|---|---|
| Login | AuthService | `authenticate(email, pwd)` | User ou None |
| Infos Employé | EmployeeService | `get_employee_by_user_id(uid)` | Employee |
| Solde Congés | EmployeeService | `get_vacation_balance(eid)` | int |
| Soumettre Demande | VacationService | `submit_vacation_request(eid, sd, ed, reason)` | VacationRequest |
| Mes Demandes | VacationService | `get_employee_vacation_requests(eid)` | List[VacationRequest] |
| Demandes Admin | VacationService | `get_pending_vacation_requests()` | List[VacationRequest] |
| Approuver | VacationService | `approve_vacation_request(rid, admin_id)` | bool |
| Rejeter | VacationService | `reject_vacation_request(rid, reason)` | bool |
| Annuler | VacationService | `cancel_vacation_request(rid)` | bool |
| Stats | VacationService | `get_employee_vacation_statistics(eid)` | dict |

---

## 🚀 Prochaines Étapes

Une fois ce backend intégré au frontend:

1. **Créer des endpoints API** (Flask/FastAPI) autour de ces services
2. **Ajouter l'authentification** (JWT tokens, sessions)
3. **Implémenter les validations** supplémentaires côté frontend
4. **Ajouter les logs** et le suivi des actions
5. **Configurer les emails** de notification
6. **Ajouter les tests** unitaires et d'intégration
