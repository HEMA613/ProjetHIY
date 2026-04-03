import json
import os

FICHIER_ADMINS = "data/admins.json"
FICHIER_DEMANDES = "data/demandes.json"


class Admin:
    """
    Classe backend représentant un administrateur.
    Peut approuver ou refuser les demandes de congé.
    """

    def __init__(self, id: int, name: str, email: str, password: str):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = "admin"

    # ------------------------------------------------------------------ #
    #  Authentification                                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def login(email: str, password: str) -> "Admin | None":
        """
        Vérifie email + mot de passe.
        Retourne l'objet Admin si correct, sinon None.
        """
        admins = Admin.charger_tous()
        for admin in admins:
            if admin.email == email and admin.password == password:
                return admin
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
    def from_dict(cls, data: dict) -> "Admin":
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
    def charger_tous() -> list["Admin"]:
        if not os.path.exists(FICHIER_ADMINS):
            return []
        with open(FICHIER_ADMINS, "r", encoding="utf-8") as f:
            return [Admin.from_dict(d) for d in json.load(f)]

    @staticmethod
    def sauvegarder_tous(admins: list["Admin"]) -> None:
        os.makedirs(os.path.dirname(FICHIER_ADMINS), exist_ok=True)
        with open(FICHIER_ADMINS, "w", encoding="utf-8") as f:
            json.dump([a.to_dict() for a in admins], f, indent=4, ensure_ascii=False)

    def sauvegarder(self) -> None:
        admins = Admin.charger_tous()
        for i, a in enumerate(admins):
            if a.id == self.id:
                admins[i] = self
                Admin.sauvegarder_tous(admins)
                return
        admins.append(self)
        Admin.sauvegarder_tous(admins)

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
                print(f"✅ Demande {demande_id} approuvée par {self.name}.")
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
        return f"Admin(id={self.id}, name='{self.name}', email='{self.email}')"