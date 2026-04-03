import json
import os

# Chemin vers le fichier JSON de stockage
FICHIER_JSON = "data/employes.json"


class Employee:
    """
    Classe backend représentant un employee.
    Gère la logique métier + la persistance JSON.
    """

    def __init__(self, id: int, name: str, email: str, role: str, vacation_balance: int = 25):
        self.id = id
        self.name = name
        self.email = email
        self.role = role                        # "employee" ou "manager"
        self.vacation_balance = vacation_balance  # solde de congés en jours

    # ------------------------------------------------------------------ #
    #  Sérialisation                                                       #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour stockage JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "vacation_balance": self.vacation_balance
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Employee":
        """Recrée un objet Employee depuis un dictionnaire JSON."""
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            role=data["role"],
            vacation_balance=data.get("vacation_balance", 25)
        )

    # ------------------------------------------------------------------ #
    #  Logique métier                                                      #
    # ------------------------------------------------------------------ #

    def deduire_solde(self, jours: int) -> None:
        """Déduit des jours du solde de congés après approbation."""
        if jours > self.vacation_balance:
            raise ValueError(f"Solde insuffisant : {self.vacation_balance}j disponibles, {jours}j demandés.")
        self.vacation_balance -= jours

    def restituer_solde(self, jours: int) -> None:
        """Restitue des jours au solde (ex: demande annulée)."""
        self.vacation_balance += jours

    def est_admin(self) -> bool:
        """Retourne True si l'employee est un administrateur."""
        return self.role == "manager"

    # ------------------------------------------------------------------ #
    #  Stockage JSON                                                       #
    # ------------------------------------------------------------------ #

    @staticmethod
    def charger_tous() -> list["Employee"]:
        """Charge tous les employees depuis le fichier JSON."""
        if not os.path.exists(FICHIER_JSON):
            return []
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            données = json.load(f)
        return [Employé.from_dict(d) for d in données]

    @staticmethod
    def sauvegarder_tous(employees: list["Employee"]) -> None:
        """Sauvegarde la liste complète des employees dans le fichier JSON."""
        os.makedirs(os.path.dirname(FICHIER_JSON), exist_ok=True)
        with open(FICHIER_JSON, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in employees], f, indent=4, ensure_ascii=False)

    def sauvegarder(self) -> None:
        """Ajoute ou met à jour cet employee dans le fichier JSON."""
        employees = Employee.charger_tous()

        # Mise à jour si l'employee existe déjà
        for i, e in enumerate(employees):
            if e.id == self.id:
                employees[i] = self
                Employee.sauvegarder_tous(employees)
                return

        # Sinon ajout
        employees.append(self)
        Employee.sauvegarder_tous(employees)

    @staticmethod
    def trouver_par_id(id: int) -> "Employee | None":
        """Recherche un employé par son ID."""
        for e in Employé.charger_tous():
            if e.id == id:
                return e
        return None

    @staticmethod
    def supprimer_par_id(id: int) -> bool:
        """Supprime un employee par son ID. Retourne True si supprimé."""
        employees = Employee.charger_tous()
        nouveaux = [e for e in employees if e.id != id]
        if len(nouveaux) == len(employees):
            return False  # pas trouvé
        Employee.sauvegarder_tous(nouveaux)
        return True

    # ------------------------------------------------------------------ #
    #  Affichage                                                           #
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:
        return (f"Employee(id={self.id}, name='{self.name}', "
                f"role='{self.role}', solde={self.vacation_balance}j)")