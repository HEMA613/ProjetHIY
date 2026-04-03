import json
import os

# Chemin vers le fichier JSON de stockage
FICHIER_JSON = "data/employes.json"


class Employé:
    """
    Classe backend représentant un employé.
    Gère la logique métier + la persistance JSON.
    """

    def __init__(self, id: int, name: str, email: str, role: str, vacation_balance: int = 25):
        self.id = id
        self.name = name
        self.email = email
        self.role = role                        # "employee" ou "admin"
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
    def from_dict(cls, data: dict) -> "Employé":
        """Recrée un objet Employé depuis un dictionnaire JSON."""
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
        """Retourne True si l'employé est un administrateur."""
        return self.role == "admin"

    # ------------------------------------------------------------------ #
    #  Stockage JSON                                                       #
    # ------------------------------------------------------------------ #

    @staticmethod
    def charger_tous() -> list["Employé"]:
        """Charge tous les employés depuis le fichier JSON."""
        if not os.path.exists(FICHIER_JSON):
            return []
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            données = json.load(f)
        return [Employé.from_dict(d) for d in données]

    @staticmethod
    def sauvegarder_tous(employés: list["Employé"]) -> None:
        """Sauvegarde la liste complète des employés dans le fichier JSON."""
        os.makedirs(os.path.dirname(FICHIER_JSON), exist_ok=True)
        with open(FICHIER_JSON, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in employés], f, indent=4, ensure_ascii=False)

    def sauvegarder(self) -> None:
        """Ajoute ou met à jour cet employé dans le fichier JSON."""
        employés = Employé.charger_tous()

        # Mise à jour si l'employé existe déjà
        for i, e in enumerate(employés):
            if e.id == self.id:
                employés[i] = self
                Employé.sauvegarder_tous(employés)
                return

        # Sinon ajout
        employés.append(self)
        Employé.sauvegarder_tous(employés)

    @staticmethod
    def trouver_par_id(id: int) -> "Employé | None":
        """Recherche un employé par son ID."""
        for e in Employé.charger_tous():
            if e.id == id:
                return e
        return None

    @staticmethod
    def supprimer_par_id(id: int) -> bool:
        """Supprime un employé par son ID. Retourne True si supprimé."""
        employés = Employé.charger_tous()
        nouveaux = [e for e in employés if e.id != id]
        if len(nouveaux) == len(employés):
            return False  # pas trouvé
        Employé.sauvegarder_tous(nouveaux)
        return True

    # ------------------------------------------------------------------ #
    #  Affichage                                                           #
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:
        return (f"Employé(id={self.id}, name='{self.name}', "
                f"role='{self.role}', solde={self.vacation_balance}j)")