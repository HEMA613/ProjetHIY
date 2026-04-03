import json
import os

FICHIER_manager = "data/manager.json"
FICHIER_DEMANDES = "data/demandes.json"


class Manager:
    """
    Classe backend représentant un manager.
    Peut approuver ou refuser les demandes de congé.
    """

    def __init__(self, id: int, name: str, email: str, password: str):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = "manager"

    # ------------------------------------------------------------------ #
    #  Authentification                                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def login(email: str, password: str) -> "Manager | None":
        """
        Vérifie email + mot de passe.
        Retourne l'objet Manager si correct, sinon None.
        """
        managers = Manager.charger_tous()
        for manager in managers:
            if manager.email == email and manager.password == password:
                return manager
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
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Manager":
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            password=data["password"]
        )

    # ------------------------------------------------------------------ #
    #  Stockage JSON                                                       #
    # ------------------------------------------------------------------ #

    @staticmethod
    def charger_tous() -> list["Manager"]:
        if not os.path.exists(FICHIER_manager):
            return []
        with open(FICHIER_manager, "r", encoding="utf-8") as f:
            return [Manager.from_dict(d) for d in json.load(f)]

    @staticmethod
    def sauvegarder_tous(managers: list["Manager"]) -> None:
        os.makedirs(os.path.dirname(FICHIER_manager), exist_ok=True)
        with open(FICHIER_manager, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in managers], f, indent=4, ensure_ascii=False)

    def sauvegarder(self) -> None:
        managers = Manager.charger_tous()
        for i, m in enumerate(managers):
            if m.id == self.id:
                managers[i] = self
                Manager.sauvegarder_tous(managers)
                return
        managers.append(self)
        Manager.sauvegarder_tous(managers)

    # ------------------------------------------------------------------ #
    #  Gestion des demandes                                                #
    # ------------------------------------------------------------------ #

    @staticmethod
    def charger_demandes() -> list[dict]:
        """Charge toutes les demandes depuis le fichier JSON."""
        if not os.path.exists(FICHIER_DEMANDES):
            return []
        with open(FICHIER_DEMANDES, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def sauvegarder_demandes(demandes: list[dict]) -> None:
        os.makedirs(os.path.dirname(FICHIER_DEMANDES), exist_ok=True)
        with open(FICHIER_DEMANDES, "w", encoding="utf-8") as f:
            json.dump(demandes, f, indent=4, ensure_ascii=False)

    def approuver_demande(self, demande_id: int) -> bool:
        """
        Approuve une demande en attente.
        Retourne True si réussi, False si demande introuvable.
        """
        demandes = self.charger_demandes()
        for d in demandes:
            if d["id"] == demande_id and d["status"] == "PENDING":
                d["status"] = "APPROVED"
                self.sauvegarder_demandes(demandes)
                print(f" Demande {demande_id} approuvée par {self.name}.")
                return True
        print(f"❌ Demande {demande_id} introuvable ou déjà traitée.")
        return False

    def refuser_demande(self, demande_id: int, motif: str = "") -> bool:
        """
        Refuse une demande en attente.
        Retourne True si réussi, False si demande introuvable.
        """
        demandes = self.charger_demandes()
        for d in demandes:
            if d["id"] == demande_id and d["status"] == "PENDING":
                d["status"] = "REJECTED"
                d["motif_refus"] = motif
                self.sauvegarder_demandes(demandes)
                print(f"❌ Demande {demande_id} refusée par {self.name}.")
                return True
        print(f"❌ Demande {demande_id} introuvable ou déjà traitée.")
        return False

    def voir_demandes_en_attente(self) -> list[dict]:
        """Retourne toutes les demandes avec statut PENDING."""
        return [d for d in self.charger_demandes() if d["status"] == "PENDING"]

    def voir_toutes_demandes(self) -> list[dict]:
        """Retourne toutes les demandes."""
        return self.charger_demandes()

    # ------------------------------------------------------------------ #
    #  Affichage                                                           #
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:
        return f"Manager(id={self.id}, name='{self.name}', email='{self.email}')"