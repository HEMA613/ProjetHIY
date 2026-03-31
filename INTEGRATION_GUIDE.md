# Integration Guide - Backend et Frontend

## 🔗 Architecture de l'Intégration

L'application utilise une architecture **API REST**:
- **Backend**: Flask API sur `http://localhost:5000`
- **Frontend**: Application Tkinter qui communique avec l'API

## 📡 Endpoints API

### Authentification
- `POST /api/login` - Connexion utilisateur
- `GET /api/users` - Liste des utilisateurs
- `GET /api/health` - Vérification API

### Employés
- `GET /api/employees` - Liste tous les employés
- `GET /api/employees/<user_id>` - Récupérer un employé
- `POST /api/employees` - Créer un employé
- `PUT /api/employees/<user_id>` - Mettre à jour un employé

### Demandes de Congés
- `GET /api/vacation-requests` - Liste des demandes
- `GET /api/vacation-requests?user_id=X` - Demandes d'un utilisateur
- `GET /api/vacation-requests?status=PENDING` - Demandes en attente
- `POST /api/vacation-requests` - Créer une demande
- `PUT /api/vacation-requests/<id>/approve` - Approuver
- `PUT /api/vacation-requests/<id>/reject` - Rejeter
- `PUT /api/vacation-requests/<id>/cancel` - Annuler

### Statistiques
- `GET /api/stats` - Statistiques globales

## 🚀 Démarrage de l'Application

### Option 1: Script Batch (Windows)
```bash
cd C:\Users\poora\Desktop\ProjetHIY
start.bat
```

### Option 2: Script Shell (Linux/Mac)
```bash
cd ~/Desktop/ProjetHIY
./start.sh
```

### Option 3: Manuel

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
pip install -r requirements.txt
python main_connected.py
```

## 🔐 Identifiants de Test

| Utilisateur | Email | Mot de passe | Rôle |
|---|---|---|---|
| Admin | admin@company.com | Azerty1234 | admin |
| User | user@company.com | Azerty1234 | employee |

## 📋 Flux de Travail

### Utilisateur Employé
1. Login avec `user@company.com`
2. Voir tableau de bord avec solde de congés
3. Créer une nouvelle demande de congés
4. Voir l'historique de ses demandes

### Utilisateur Admin
1. Login avec `admin@company.com`
2. Voir tous les employés
3. Voir les demandes en attente
4. Approuver ou rejeter les demandes
5. Consulter les statistiques

## 🔧 Fichiers Clés

- `backend/api.py` - API Flask complète
- `frontend/main_connected.py` - Interface GUI connectée
- `backend/Models/` - Modèles de données
- `backend/Services/` - Logique métier
- `backend/Database/` - Gestion SQLite

## 📝 Requêtes Exemple

### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@company.com","password":"Azerty1234"}'
```

### Créer une demande
```bash
curl -X POST http://localhost:5000/api/vacation-requests \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id":2,
    "start_date":"2026-04-05",
    "end_date":"2026-04-10",
    "reason":"Vacances familiales"
  }'
```

### Approuver une demande
```bash
curl -X PUT http://localhost:5000/api/vacation-requests/1/approve \
  -H "Content-Type: application/json" \
  -d '{"approved_by":"admin"}'
```

## ✅ Checklist d'Intégration

- ✅ API REST complète avec tous les endpoints
- ✅ Frontend Tkinter connecté à l'API
- ✅ Authentification fonctionnelle
- ✅ CRUD pour employés et demandes
- ✅ Gestion des rôles (admin/employee)
- ✅ Validation des données
- ✅ Scripts de démarrage automatisés
- ✅ Support CORS pour requêtes cross-origin

## 🐛 Troubleshooting

**L'API ne démarre pas:**
```bash
# Vérifier que le port 5000 est libre
netstat -ano | findstr :5000
# Ou tuer le processus
taskkill /PID <PID> /F
```

**Erreur de connexion API:**
- Vérifier que l'API démarre correctement
- Vérifier que le port 5000 est accessible
- Vérifier les logs dans le terminal du backend

**Erreur de dépendances:**
```bash
# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

## 📞 Support

Pour plus d'informations, consultez:
- Backend: `backend/README.md`
- Architecture: `backend/ARCHITECTURE_UML.md`
- Models: `backend/Models/`
