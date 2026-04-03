from admin import Admin
from utilisateur import Utilisateur

class Gestionnaire:
    """
    Classe centrale du backend.
    C'est le seul fichier que l'interface Tkinter doit appeler.
    """

    # ------------------------------------------------------------------ #
    #  Authentification                                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def login(email: str, password: str) -> dict | None:
        """
        Tente de connecter un utilisateur (admin ou employé).
        Retourne un dictionnaire avec l'objet et son rôle, ou None si échec.

        Exemple de retour :
            {"role": "admin",    "user": <Admin>}
            {"role": "employee", "user": <Utilisateur>}
        """
        # On vérifie d'abord si c'est un admin
        admin = Admin.login(email, password)
        if admin:
            print(f"🔐 Connexion admin : {admin.name}")
            return {"role": "admin", "user": admin}

        # Sinon on vérifie si c'est un employé
        user = Utilisateur.login(email, password)
        if user:
            print(f"🔐 Connexion employé : {user.name}")
            return {"role": "employee", "user": user}

        print("❌ Email ou mot de passe incorrect.")
        return None

    # ------------------------------------------------------------------ #
    #  Gestion des demandes (Admin)                                        #
    # ------------------------------------------------------------------ #

    @staticmethod
    def approuver_demande(admin: Admin, demande_id: int) -> bool:
        """
        Approuve une demande et déduit les jours du solde de l'employé.
        """
        demandes = Admin.charger_demandes()

        for d in demandes:
            if d["id"] == demande_id and d["status"] == "PENDING":

                # Déduire le solde de l'employé
                employe = Utilisateur.charger_tous()
                for u in employe:
                    if u.id == d["employee_id"]:
                        try:
                            u.deduire_solde(d["days"])
                            u.sauvegarder()
                        except ValueError as e:
                            print(f"❌ Impossible d'approuver : {e}")
                            return False

                # Approuver la demande
                return admin.approuver_demande(demande_id)

        print(f"❌ Demande {demande_id} introuvable ou déjà traitée.")
        return False

    @staticmethod
    def refuser_demande(admin: Admin, demande_id: int, motif: str = "") -> bool:
        """
        Refuse une demande (le solde n'est pas modifié).
        """
        return admin.refuser_demande(demande_id, motif)

    @staticmethod
    def demandes_en_attente() -> list[dict]:
        """Retourne toutes les demandes en attente (PENDING)."""
        return Admin.charger_demandes().__class__(
            [d for d in Admin.charger_demandes() if d["status"] == "PENDING"]
        )

    @staticmethod
    def toutes_les_demandes() -> list[dict]:
        """Retourne toutes les demandes."""
        return Admin.charger_demandes()

    # ------------------------------------------------------------------ #
    #  Gestion des demandes (Employé)                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def soumettre_demande(user: Utilisateur, start_date, end_date, reason: str = "") -> dict | None:
        """
        Soumet une demande de congé pour un employé.
        Retourne la demande créée ou None si erreur.
        """
        try:
            return user.soumettre_demande(start_date, end_date, reason)
        except ValueError as e:
            print(f"❌ Erreur : {e}")
            return None

    @staticmethod
    def mes_demandes(user: Utilisateur) -> list[dict]:
        """Retourne les demandes de l'employé connecté."""
        return user.mes_demandes()

    @staticmethod
    def annuler_demande(user: Utilisateur, demande_id: int) -> bool:
        """Annule une demande en attente de l'employé connecté."""
        return user.annuler_demande(demande_id)

    # ------------------------------------------------------------------ #
    #  Statistiques                                                        #
    # ------------------------------------------------------------------ #

    @staticmethod
    def statistiques() -> dict:
        """
        Retourne un résumé global pour le tableau de bord admin.

        Exemple de retour :
        {
            "total_demandes": 10,
            "en_attente": 3,
            "approuvees": 5,
            "refusees": 2,
            "total_employes": 4
        }
        """
        demandes = Admin.charger_demandes()
        employes = Utilisateur.charger_tous()

        stats = {
            "total_demandes": len(demandes),
            "en_attente":     sum(1 for d in demandes if d["status"] == "PENDING"),
            "approuvees":     sum(1 for d in demandes if d["status"] == "APPROVED"),
            "refusees":       sum(1 for d in demandes if d["status"] == "REJECTED"),
            "annulees":       sum(1 for d in demandes if d["status"] == "CANCELLED"),
            "total_employes": len(employes)
        }

        print(f"📊 Stats : {stats}")
        return stats

    @staticmethod
    def solde_employe(employe_id: int) -> int | None:
        """Retourne le solde de congés d'un employé par son ID."""
        employes = Utilisateur.charger_tous()
        for u in employes:
            if u.id == employe_id:
                return u.vacation_balance
        return None

    @staticmethod
    def liste_employes() -> list[dict]:
        """Retourne la liste de tous les employés avec leur solde."""
        return [u.to_dict() for u in Utilisateur.charger_tous()]