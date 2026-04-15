# Résumé du Code - Projet Gestion des Congés

## Vue d'ensemble
Ce projet est une application de gestion des congés développée en Python avec Tkinter pour l'interface graphique. Il utilise une architecture backend/frontend avec des fichiers JSON pour la persistance des données.

## Structure du Projet
```
ProjetHIY/
├── maintest.py              # Point d'entrée principal avec LoginForm
├── backend/                 # Logique métier et données
│   ├── auth_service.py      # Service d'authentification
│   ├── employee.py          # Classe Employee
│   ├── manager.py           # Classe Manager
│   ├── init_data.py         # Initialisation des données
│   ├── data/                # Fichiers JSON de données
│   │   ├── employes.json    # Données des employés
│   │   ├── manager.json     # Données des managers
│   │   └── demandes.json    # Demandes de congés
│   └── ...
├── frontend/                # Interfaces utilisateur
│   ├── manager_dashboard.py # Dashboard du manager
│   ├── employee_dashboard.py # Dashboard de l'employé
│   └── services/
│       └── vacation_service.py # Service de gestion des congés
└── ...
```

## Flux d'Application
1. **Login** : `maintest.py` lance `LoginForm` pour authentification
2. **Dashboard** : Selon le rôle (manager/employee), ouvre le dashboard approprié
3. **Gestion** : Utilisation des services pour gérer les congés
4. **Déconnexion** : Retour à l'écran de login

## Classes Principales

### Backend
- **Employee/Manager** : Classes pour les utilisateurs avec méthodes de sauvegarde/chargement
- **Gestionnaire** : Classe statique pour l'authentification et gestion des demandes
- **VacationService** : Service pour les opérations CRUD sur les congés

### Frontend
- **LoginForm** : Formulaire de connexion avec validation
- **ManagerDashboard** : Interface manager avec onglets (Demandes, Calendrier, Employés)
- **EmployeeDashboard** : Interface employé avec onglets (Accueil, Nouvelle demande, Calendrier)

## Données
- **employes.json** : Liste des employés avec email, nom, mot de passe, solde congés
- **manager.json** : Liste des managers (similaire)
- **demandes.json** : Liste des demandes avec id, employé, dates, statut, etc.

## Fonctionnalités Clés
- Authentification par email/mot de passe
- Soumission de demandes de congés
- Approbation/rejet par manager
- Visualisation du calendrier
- Statistiques des congés
- Déconnexion avec retour au login

## Points d'Entrée
- `python maintest.py` : Lance l'application complète
- `python backend/test_backend.py` : Tests unitaires du backend
- `python backend/init_data.py` : Initialise les données d'exemple

## Dépendances
- Python 3.x
- Tkinter (inclus dans Python standard)
- Modules standard : json, os, datetime, calendar

## Architecture
- **MVC-like** : Backend (modèle), Frontend (vue), Services (contrôleur)
- **Séparation** : Logique métier séparée de l'UI
- **Persistance** : JSON pour simplicité (pas de base de données)
- **Callbacks** : Utilisation de callbacks pour la déconnexion

Ce résumé permet de comprendre la structure globale sans plonger dans le code détaillé.

#Questions possibles:

1- Affichez un raccourci de l'identifiants email et mot de passe sur le page pour se  connecter rapidement en clic.

2- Modifiez l'entree de date dans la section de faire un nouveau demande en calandrier.

3- Ajoutez un boutton pour approuver et accepter les demandes dans le manager dashboard.

4-

5-
