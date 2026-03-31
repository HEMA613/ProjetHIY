# 🏢 Vacation Manager - Gestionnaire de Congés

Système complet de gestion des demandes de congés avec **Backend API REST** et **Frontend GUI Tkinter**.

---

## 📋 Table des matières

- [Architecture](#architecture)
- [Installation](#installation)
- [Démarrage Rapide](#démarrage-rapide)
- [Identifiants de Test](#identifiants-de-test)
- [Utilisation](#utilisation)
- [Structure du Projet](#structure-du-projet)
- [API REST](#api-rest)
- [Troubleshooting](#troubleshooting)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│          Frontend GUI (Tkinter)                     │
│  - Dashboard personnalisé                          │
│  - Gestion des demandes de congés                  │
│  - Interface Admin avec approbations               │
└───────────────────────┬─────────────────────────────┘
                        │
                   HTTP Requests
                        │
┌───────────────────────▼─────────────────────────────┐
│          Backend API REST (Flask)                   │
│  - http://localhost:5000/api                       │
│  - Authentification, CRUD, Validation              │
└───────────────────────┬─────────────────────────────┘
                        │
                   SQL Queries
                        │
┌───────────────────────▼─────────────────────────────┐
│          Base de Données (SQLite)                   │
│  - vacation_manager.db                             │
│  - Tables: users, employees, vacation_requests     │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 Installation

### Prérequis

- Python 3.7+
- pip (Python Package Manager)
- Windows/Linux/macOS

### Étapes d'Installation

1. **Cloner/Télécharger le projet**
```bash
cd C:\Users\YourUser\Desktop\ProjetHIY
```

2. **Installer les dépendances Backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Installer les dépendances Frontend**
```bash
cd ../frontend
pip install -r requirements.txt
```

---

## 🚀 Démarrage Rapide

### Option 1: Script Automatisé (Recommandé)

**Windows:**
```bash
start.bat
```

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Démarrage Manuel

**Terminal 1 - Backend API:**
```bash
cd backend
python api.py
```

L'API démarre sur `http://localhost:5000`

**Terminal 2 - Frontend GUI:**
```bash
cd frontend
python main_connected.py
```

L'interface GUI s'ouvre automatiquement

---

## 🔐 Identifiants de Test

| Rôle | Email | Mot de passe | Fonction |
|------|-------|---------|----------|
| **Admin** | `admin@company.com` | `Azerty1234` | Approuver/Rejeter les demandes |
| **Employé** | `user@company.com` | `Azerty1234` | Soumettre les demandes |

---

## 📖 Utilisation

### Pour un Employé

1. **Connexions**
   - Email: `user@company.com`
   - Mot de passe: `Azerty1234`

2. **Dashboard**
   - Voir solde de congés disponibles
   - Voir l'historique des demandes

3. **Créer une Demande**
   - Cliquer sur "Nouvelle Demande de Congés"
   - Sélectionner les dates
   - Ajouter une raison
   - Soumettre

4. **Suivi des Demandes**
   - Onglet "Mes Demandes"
   - Voir statut: PENDING, APPROVED, REJECTED

### Pour un Admin

1. **Connexion**
   - Email: `admin@company.com`
   - Mot de passe: `Azerty1234`

2. **Dashboard Admin**
   - See all employees
   - Review approval requests

3. **Gérer les Demandes**
   - Onglet "Admin"
   - Voir les demandes en attente
   - Approuver: Déduit les jours du solde
   - Rejeter: Permet de justifier

4. **Managemen des Employés**
   - Voir la liste des employés
   - Consulter leurs soldes

---

## 📁 Structure du Projet

```
ProjetHIY/
├── backend/
│   ├── Models/                 # Modèles de données
│   │   ├── user.py            # Utilisateur (Admin/Employee)
│   │   ├── employee.py        # Profil employé + solde
│   │   └── vacation_request.py # Demande de congés
│   ├── Database/              # Gestion SQLite
│   │   └── database_manager.py
│   ├── Services/              # Logique métier
│   │   ├── auth_service.py    # Authentification
│   │   ├── employee_service.py
│   │   └── vacation_service.py
│   ├── api.py                 # API Flask REST
│   ├── app.py                 # Tests backend
│   ├── requirements.txt       # Dépendances Flask
│   └── vacation_manager.db    # Base de données
│
├── frontend/
│   ├── main_connected.py      # GUI Tkinter (connectée)
│   ├── main.py                # GUI Tkinter (ancienne)
│   ├── requirements.txt       # Dépendances requests
│   └── Models/, services/     # Modèles utilisés
│
├── test_integration.py        # Tests d'intégration
├── start.bat                  # Démarrage automatisé (Windows)
├── start.sh                   # Démarrage automatisé (Linux/Mac)
└── README.md                  # Ce fichier
```

---

## 🔌 API REST

### Base URL
```
http://localhost:5000/api
```

### Endpoints Principaux

#### Authentification
```bash
POST /api/login
Content-Type: application/json

{
  "email": "user@company.com",
  "password": "Azerty1234"
}
```

#### Employés
```bash
GET /api/employees                           # Tous les employés
GET /api/employees/<user_id>                 # Un employé
POST /api/employees                          # Créer un employé
PUT /api/employees/<user_id>                 # Modifier un employé
```

#### Demandes de Congés
```bash
GET /api/vacation-requests                   # Toutes les demandes
GET /api/vacation-requests?user_id=2         # Pour un utilisateur
GET /api/vacation-requests?status=PENDING    # Demandes en attente

POST /api/vacation-requests                  # Créer une demande
{
  "employee_id": 1,
  "start_date": "2026-04-05",
  "end_date": "2026-04-10",
  "reason": "Vacances"
}

PUT /api/vacation-requests/<id>/approve      # Approuver
PUT /api/vacation-requests/<id>/reject       # Rejeter
PUT /api/vacation-requests/<id>/cancel       # Annuler
```

#### Statistiques
```bash
GET /api/stats                               # Stats globales
GET /api/health                              # Health check
```

---

## ✅ Tests

### Exécuter les Tests d'Intégration

```bash
python test_integration.py
```

**Résultat attendu:**
```
✓ Authentification                    [RÉUSSI]
✓ Gestion des employés               [RÉUSSI]
✓ Validation des dates                [RÉUSSI]
✓ Calcul des jours                    [RÉUSSI]
✓ Vérification du solde               [RÉUSSI]
✓ Demandes de congés                  [RÉUSSI]
✓ Endpoints API                       [RÉUSSI]
```

---

## 🐛 Troubleshooting

### Erreur: "Impossible de se connecter à l'API backend"

**Solution:**
1. Vérifier que l'API démarre sans erreur
2. Vérifier que le port 5000 est libre
3. Attendre 2-3 secondes après le démarrage de l'API

### Erreur: "Port 5000 déjà utilisé"

```bash
# Windows: Trouver le processus
netstat -ano | findstr :5000

# Tuer le processus
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Erreur: "Module not found: requests"

```bash
pip install requests
```

### Erreur: "Module not found: Flask"

```bash
cd backend
pip install -r requirements.txt
```

### La base de données est corrompue

```bash
# Supprimer la BD et la recréer
rm vacation_manager.db
# Relancer l'API
```

---

## 📊 Schéma de Base de Données

```sql
-- Utilisateurs (Admin/Employee)
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT CHECK (role IN ('admin', 'employee'))
);

-- Employés
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE,
    name TEXT,
    email TEXT,
    department TEXT,
    vacation_balance INTEGER DEFAULT 20,
    vacation_used INTEGER DEFAULT 0
);

-- Demandes de Congés
CREATE TABLE vacation_requests (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    start_date DATE,
    end_date DATE,
    days_count INTEGER,
    reason TEXT,
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    approved_by INTEGER,
    rejection_reason TEXT
);
```

---

## 🎯 Fonctionnalités

### ✅ Implémentées
- [x] Authentification (Admin + Employee)
- [x] Gestion des profils employés
- [x] Création de demandes de congés
- [x] Validation des dates
- [x] Calcul des jours ouvrables
- [x] Approbation/Rejet des demandes
- [x] Gestion du solde de congés
- [x] Dashboard personnalisé par rôle
- [x] API REST complète
- [x] Base de données SQLite
- [x] Interface GUI Tkinter
- [x] Tests d'intégration

### 📋 Futures Améliorations
- [ ] Historique des modifications
- [ ] Notifications par email
- [ ] Calendrier visuel
- [ ] Intégration LDAP/Active Directory
- [ ] Export en PDF
- [ ] Interface web (Django/React)

---

## 📞 Support

### Logs
Les logs de l'API sont affichés dans le terminal lors du démarrage.

### Fichiers de Donnée
- Base de données: `backend/vacation_manager.db`
- Fichiers de configuration: `backend/*.py`

### Documentation Technique
- [`backend/README.md`](backend/README.md) - Documentation backend
- [`backend/ARCHITECTURE_UML.md`](backend/ARCHITECTURE_UML.md) - Diagrammes UML
- [`backend/INTEGRATION_GUIDE.md`](backend/INTEGRATION_GUIDE.md) - Guide d'intégration

---

## 📜 Licence

Projet développé par Personne 1 (Backend & Modèles)

---

## ✨ Résumé

| Aspect | Détail |
|--------|--------|
| **Langage Backend** | Python 3 |
| **Framework API** | Flask 2.3 |
| **Interface Frontend** | Tkinter |
| **Base de Données** | SQLite |
| **Authentification** | Email + Mot de passe sécurisé |
| **Architecture** | API REST + GUI Desktop |
| **Tests** | Tests d'intégration complets |
| **Statut** | ✅ Production Ready |

---

**Mise à jour:** 31 Mars 2026
**Version:** 1.0.0
