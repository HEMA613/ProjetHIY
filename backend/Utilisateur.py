import json
import os
from datetime import date

FICHIER_EMPLOYES = "data/employes.json"
FICHIER_DEMANDES = "data/demandes.json"


class Utilisateur:
    """
    Classe backend représentant un employé connecté.
    Peut soumettre et consulter ses propres demandes de congé.
    """

    def __init__(self, id: int, name: str, email: str, password: str, vacation_balance: int = 25):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.vacation_balance = vacation_balance
        self.role = "employee"

    # ------------------------------------------------------------------ #
    #  Authentification                                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def login(email: str, password: str) -> "Utilisateur | None":
        """
        Vérifie email + mot de passe.
        Retourne l'objet Utilisateur si correct, sinon None.
        """
        utilisateurs = Utilisateur.charger_tous()
        for u in utilisateurs:
            if u.email == email and u.password == password:
                return u
        return None

    # ------------------------------------------------------------------ #
    #  Sérialisation                                                       #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "vacation_balance": self.vacation_balance,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Utilisateur":
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            password=data["password"],
            vacation_balance=data.get("vacation_balance", 25)
        )

    # ------------------------------------------------------------------ #
    #  Stockage JSON                                                       #
    # ------------------------------------------------------------------ #

    @staticmethod
    def charger_tous() -> list["Utilisateur"]:
        if not os.path.exists(FICHIER_EMPLOYES):
            return []
        with open(FICHIER_EMPLOYES, "r", encoding="utf-8") as f:
            données = json.load(f)
        # On filtre uniquement les employés (pas les admins)
        return [Utilisateur.from_dict(d) for d in données if d.get("role") == "employee"]

    @staticmethod
    def sauvegarder_tous(utilisateurs: list["Utilisateur"]) -> None:
        os.makedirs(os.path.dirname(FICHIER_EMPLOYES), exist_ok=True)
        with open(FICHIER_EMPLOYES, "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in utilisateurs], f, indent=4, ensure_ascii=False)

    def sauvegarder(self) -> None:
        utilisateurs = Utilisateur.charger_tous()
        for i, u in enumerate(utilisateurs):
            if u.id == self.id:
                utilisateurs[i] = self
                Utilisateur.sauvegarder_tous(utilisateurs)
                return
        utilisateurs.append(self)
        Utilisateur.sauvegarder_tous(utilisateurs)

    @staticmethod
    def trouver_par_id(id: int) -> "Utilisateur | None":
        """Recherche un utilisateur par son ID."""
        for u in Utilisateur.charger_tous():
            if u.id == id:
                return u
        return None

    # ------------------------------------------------------------------ #
    #  Demandes de congé                                                   #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _charger_demandes() -> list[dict]:
        if not os.path.exists(FICHIER_DEMANDES):
            return []
        with open(FICHIER_DEMANDES, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _sauvegarder_demandes(demandes: list[dict]) -> None:
        os.makedirs(os.path.dirname(FICHIER_DEMANDES), exist_ok=True)
        with open(FICHIER_DEMANDES, "w", encoding="utf-8") as f:
            json.dump(demandes, f, indent=4, ensure_ascii=False)

    def soumettre_demande(self, start_date: date, end_date: date, reason: str = "") -> dict:
        """
        Soumet une nouvelle demande de congé.
        Vérifie les dates et le solde disponible.
        Retourne la demande créée sous forme de dictionnaire.
        """
        # Validation des dates
        if start_date > end_date:
            raise ValueError("La date de début doit être avant la date de fin.")

        # Calcul de la durée
        days = (end_date - start_date).days + 1

        # Vérification du solde
        if days > self.vacation_balance:
            raise ValueError(f"Solde insuffisant : {self.vacation_balance}j disponibles, {days}j demandés.")

        # Création de la demande
        demandes = self._charger_demandes()
        nouvel_id = max((d["id"] for d in demandes), default=0) + 1

        nouvelle_demande = {
            "id": nouvel_id,
            "employee_id": self.id,
            "employee_name": self.name,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "days": days,
            "reason": reason,
            "status": "PENDING"
        }

        demandes.append(nouvelle_demande)
        self._sauvegarder_demandes(demandes)
        print(f"📋 Demande soumise : {days}j du {start_date} au {end_date}.")
        return nouvelle_demande

    def mes_demandes(self) -> list[dict]:
        """Retourne uniquement les demandes de cet utilisateur."""
        return [d for d in self._charger_demandes() if d["employee_id"] == self.id]

    def deduire_solde(self, jours: int) -> None:
        """Déduit des jours du solde après approbation."""
        if jours > self.vacation_balance:
            raise ValueError(f"Solde insuffisant : {self.vacation_balance}j disponibles, {jours}j demandés.")
        self.vacation_balance -= jours

    def annuler_demande(self, demande_id: int) -> bool:
        """
        Annule une demande en attente.
        Retourne True si réussi.
        """
        demandes = self._charger_demandes()
        for d in demandes:
            if d["id"] == demande_id and d["employee_id"] == self.id and d["status"] == "PENDING":
                d["status"] = "CANCELLED"
                self._sauvegarder_demandes(demandes)
                print(f"🚫 Demande {demande_id} annulée.")
                return True
        print(f"❌ Demande {demande_id} introuvable ou non annulable.")
        return False

    # ------------------------------------------------------------------ #
    #  Affichage                                                           #
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:
        return (f"Utilisateur(id={self.id}, name='{self.name}', "
                f"email='{self.email}', solde={self.vacation_balance}j)")