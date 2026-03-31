# 📊 Diagramme UML - Architecture du Backend

## Diagramme de Classes

```mermaid
classDiagram
    class User {
        -int id
        -string username
        -string email
        -string password
        -string role
        -datetime created_at
        -bool is_active
        +to_dict() dict
        +from_dict(dict) User
    }

    class Employee {
        -int id
        -int user_id
        -string name
        -string email
        -string department
        -string position
        -int vacation_balance
        -int vacation_used
        -datetime hire_date
        -datetime created_at
        +get_vacation_available() int
        +has_enough_balance(days: int) bool
        +use_vacation_days(days: int) bool
        +refund_vacation_days(days: int) void
        +to_dict() dict
        +from_dict(dict) Employee
    }

    class VacationRequest {
        -int id
        -int employee_id
        -datetime start_date
        -datetime end_date
        -string reason
        -VacationStatus status
        -int days_count
        -datetime created_at
        -datetime updated_at
        -int approved_by
        -string rejection_reason
        +calculate_days() int
        +is_valid() bool
        +approve(admin_id: int) void
        +reject(reason: string) void
        +cancel() void
        +to_dict() dict
        +from_dict(dict) VacationRequest
    }

    class VacationStatus {
        <<enumeration>>
        PENDING
        APPROVED
        REJECTED
        CANCELLED
    }

    class DatabaseManager {
        -string db_path
        +get_connection() Connection
        +init_database() void
        +create_user() User
        +get_user_by_id(id: int) User
        +get_user_by_email(email: str) User
        +create_employee() Employee
        +get_employee_by_id(id: int) Employee
        +get_employee_by_user_id(user_id: int) Employee
        +create_vacation_request() VacationRequest
        +get_vacation_request_by_id(id: int) VacationRequest
        +get_vacation_requests_by_employee(emp_id: int) List
        +get_all_pending_vacation_requests() List
        +update_vacation_request_status() void
    }

    class AuthService {
        -DatabaseManager db
        +authenticate(email: str, password: str) User
        +create_user() User
        +get_user() User
        +is_admin(user_id: int) bool
        +is_employee(user_id: int) bool
    }

    class EmployeeService {
        -DatabaseManager db
        +create_employee() Employee
        +get_employee() Employee
        +get_employee_by_user_id() Employee
        +get_all_employees() List
        +get_vacation_balance() int
        +get_vacation_details() dict
        +use_vacation_days() bool
        +refund_vacation_days() bool
        +has_enough_vacation() bool
        +get_employee_info() dict
    }

    class VacationService {
        -DatabaseManager db
        +submit_vacation_request() VacationRequest
        +get_vacation_request() VacationRequest
        +get_employee_vacation_requests() List
        +get_pending_vacation_requests() List
        +get_all_vacation_requests() List
        +approve_vacation_request() bool
        +reject_vacation_request() bool
        +cancel_vacation_request() bool
        +get_vacation_request_details() dict
        +get_employee_vacation_statistics() dict
    }

    class VacationManagerApp {
        -DatabaseManager db
        -AuthService auth_service
        -EmployeeService employee_service
        -VacationService vacation_service
        +test_authentication() void
        +test_employee_management() void
        +test_vacation_request() void
        +run_tests() void
    }

    %% Relations
    User "1" -- "1" Employee : has_profile
    Employee "1" -- "*" VacationRequest : creates
    VacationRequest "1" -- "1" VacationStatus : has_status
    
    AuthService "1" -- "1" DatabaseManager : uses
    EmployeeService "1" -- "1" DatabaseManager : uses
    VacationService "1" -- "1" DatabaseManager : uses
    
    VacationManagerApp "1" -- "1" AuthService : uses
    VacationManagerApp "1" -- "1" EmployeeService : uses
    VacationManagerApp "1" -- "1" VacationService : uses
    VacationManagerApp "1" -- "1" DatabaseManager : initializes
```

## Diagramme de Flux - Processus de Demande de Congés

```mermaid
sequenceDiagram
    participant U as Utilisateur
    participant F as Frontend
    participant B as Backend
    participant DB as Database

    U->>F: Remplit formulaire de congés
    F->>B: POST /vacation/submit
    B->>B: Valide les dates
    B->>DB: Vérifie le solde
    alt Solde suffisant
        B->>DB: Crée VacationRequest (PENDING)
        B->>F: Retourne succès
        F->>U: Affiche confirmation
    else Solde insuffisant
        B->>F: Retourne erreur
        F->>U: Affiche message d'erreur
    end

    Note over U: Admin consulte les demandes

    U->>F: Consulte demandes en attente
    F->>B: GET /vacation/pending
    B->>DB: Récupère PENDING requests
    B->>F: Retourne liste
    F->>U: Affiche demandes

    U->>F: Approuve ou rejette
    alt Approuvé
        F->>B: POST /vacation/approve
        B->>DB: Vérifie l'employé
        B->>DB: Met à jour statut = APPROVED
        B->>DB: Utilise jours de congés
        B->>DB: Met à jour vacation_used
    else Rejeté
        F->>B: POST /vacation/reject
        B->>DB: Met à jour statut = REJECTED
        B->>DB: Ajoute motif du rejet
    end
    B->>F: Retourne succès
    F->>U: Affiche confirmation
```

## Diagramme d'État - Demande de Congés

```mermaid
stateDiagram-v2
    [*] --> PENDING: Créer demande
    
    PENDING --> APPROVED: Admin approuve
    PENDING --> REJECTED: Admin rejette
    PENDING --> CANCELLED: Employé annule
    
    APPROVED --> CANCELLED: Employé annule
    
    REJECTED --> [*]: Fin (données conservées)
    CANCELLED --> [*]: Fin (congés remboursés)
    APPROVED --> [*]: Fin (congés utilisés)
```

## Architecture en Couches

```
┌─────────────────────────────────────┐
│         Frontend (React)             │
│  (Interfaces Figma)                  │
└──────────────┬──────────────────────┘
               │ API HTTP/JSON
┌──────────────▼──────────────────────┐
│         Services Layer               │
│  - AuthService                       │
│  - EmployeeService                   │
│  - VacationService                   │
└──────────────┬──────────────────────┘
               │ Métier
┌──────────────▼──────────────────────┐
│         Models/Domain Layer          │
│  - User                              │
│  - Employee                          │
│  - VacationRequest                   │
└──────────────┬──────────────────────┘
               │ Persistance
┌──────────────▼──────────────────────┐
│      Database Manager                │
│  (SQLite - vacation_manager.db)      │
└──────────────┬──────────────────────┘
               │ SQL
┌──────────────▼──────────────────────┐
│          SQLite Database             │
│  - users                             │
│  - employees                         │
│  - vacation_requests                 │
└─────────────────────────────────────┘
```

## Package Diagram

```mermaid
graph TB
    subgraph Backend["Backend Package"]
        subgraph Models["Models"]
            U["User"]
            E["Employee"]
            VR["VacationRequest"]
            VS["VacationStatus"]
        end
        
        subgraph Database["Database"]
            DM["DatabaseManager"]
        end
        
        subgraph Services["Services"]
            AS["AuthService"]
            ES["EmployeeService"]
            VAS["VacationService"]
        end
        
        subgraph App["Application"]
            MA["VacationManagerApp"]
        end
    end
    
    AS -->|uses| DM
    ES -->|uses| DM
    VAS -->|uses| DM
    
    AS -->|manages| U
    ES -->|manages| E
    VAS -->|manages| VR
    
    MA -->|orchestrates| AS
    MA -->|orchestrates| ES
    MA -->|orchestrates| VAS
    
    VR -->|uses| VS
    E -->|relates_to| U
```

## Modèle de Données - Schema SQLite

```mermaid
erDiagram
    USERS ||--o{ EMPLOYEES : "1:1"
    EMPLOYEES ||--o{ VACATION_REQUESTS : "1:many"
    USERS ||--o{ VACATION_REQUESTS : "approves"
    
    USERS {
        int id PK
        string username UK
        string email UK
        string password
        string role
        string created_at
        boolean is_active
    }
    
    EMPLOYEES {
        int id PK
        int user_id FK
        string name
        string email
        string department
        string position
        int vacation_balance
        int vacation_used
        string hire_date
        string created_at
    }
    
    VACATION_REQUESTS {
        int id PK
        int employee_id FK
        string start_date
        string end_date
        string reason
        string status
        int days_count
        string created_at
        string updated_at
        int approved_by FK
        string rejection_reason
    }
```

## Flux d'Authentification

```mermaid
graph LR
    A["Frontend: Login"] -->|email + password| B["AuthService.authenticate()"]
    B -->|query by email| C["DatabaseManager"]
    C -->|SELECT user| D["SQLite DB"]
    D -->|return User| C
    C -->|return User| B
    B -->|verify password| E{Match?}
    E -->|No| F["Return None"]
    E -->|Yes & Active| G["Return User"]
    G -->|user + role| H["Frontend: Dashboard"]
    F -->|Failed| I["Frontend: Error"]
```

## Flux de Gestion des Congés

```mermaid
graph TD
    A["Employé: Demande"] -->|dates + motif| B["VacationService.submit()"]
    B -->|valide| C{Dates valides?}
    C -->|Non| K["Erreur: dates invalides"]
    C -->|Oui| D["Récupère Employee"]
    D -->|vérifie solde| E{Solde suffisant?}
    E -->|Non| L["Erreur: solde insuffisant"]
    E -->|Oui| F["Crée VacationRequest PENDING"]
    F -->|save| G["Database"]
    G -->|confirmation| H["Frontend: Succès"]
    
    I["Admin: Console"] -->|voit| J["get_pending_vacation_requests()"]
    J -->|retourne liste| I
    I -->|approuve/rejette| M["approve/reject_vacation_request()"]
    M -->|mise à jour| G
    M -->|update employee| N["use_vacation_days()"]
    N -->|save| G
```

Maintes correspondances avec les spécifications:
- ✅ Classes Python bien structurées
- ✅ POO avec encapsulation
- ✅ Relations cohérentes
- ✅ Gestion centralisée des données
- ✅ Services métier découplés
- ✅ Architecture en couches
