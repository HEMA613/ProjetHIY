from .manager import Manager
from .Utilisateur import Employee

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
        Tente de connecter un utilisateur (manager ou employee).
        Retourne un dictionnaire avec l'objet et son rôle, ou None si échec.

        Exemple de retour :
            {"role": "manager",    "user": <Manager>}
            {"role": "employee", "user": <Employee>}
        """
        # On vérifie d'abord si c'est un manager
        manager = Manager.login(email, password)
        if manager:
            print(f"🔐 Connexion manager : {manager.name}")
            return {"role": "manager", "user": manager}

        # Sinon on vérifie si c'est un employee
        user = Employee.login(email, password)
        if user:
            print(f"🔐 Connexion employee : {user.name}")
            return {"role": "employee", "user": user}

        print("❌ Email ou mot de passe incorrect.")
        return None

    # ------------------------------------------------------------------ #
    #  Gestion des demandes (Manager)                                        #
    # ------------------------------------------------------------------ #

    @staticmethod
    def approuver_demande(manager: Manager, demande_id: int) -> bool:
        """
        Approuve une demande et déduit les jours du solde de l'employee.
        """
        demandes = Manager.charger_demandes()

        for d in demandes:
            if d["id"] == demande_id and d["status"] == "PENDING":

                # Déduire le solde de l'employee
                employee = Employee.charger_tous()
                for u in employee:
                    if u.id == d["employee_id"]:
                        try:
                            u.deduire_solde(d["days"])
                            u.sauvegarder()
                        except ValueError as e:
                            print(f"❌ Impossible d'approuver : {e}")
                            return False

                # Approuver la demande
                return manager.approuver_demande(demande_id)

        print(f"❌ Demande {demande_id} introuvable ou déjà traitée.")
        return False

    @staticmethod
    def refuser_demande(manager: Manager, demande_id: int, motif: str = "") -> bool:
        """
        Refuse une demande (le solde n'est pas modifié).
        """
        return manager.refuser_demande(demande_id, motif)

    @staticmethod
    def demandes_en_attente() -> list[dict]:
        """Retourne toutes les demandes en attente (PENDING)."""
        return Manager.charger_demandes().__class__(
            [d for d in Manager.charger_demandes() if d["status"] == "PENDING"]
        )

    @staticmethod
    def toutes_les_demandes() -> list[dict]:
        """Retourne toutes les demandes."""
        return Manager.charger_demandes()

    # ------------------------------------------------------------------ #
    #  Gestion des demandes (Employee)                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def soumettre_demande(user: Employee, start_date, end_date, reason: str = "") -> dict | None:
        """
        Soumet une demande de congé pour un employee.
        Retourne la demande créée ou None si erreur.
        """
        try:
            return user.soumettre_demande(start_date, end_date, reason)
        except ValueError as e:
            print(f"❌ Erreur : {e}")
            return None

    @staticmethod
    def mes_demandes(user: Employee) -> list[dict]:
        """Retourne les demandes de l'employee connecté."""
        return user.mes_demandes()

    @staticmethod
    def annuler_demande(user: Employee, demande_id: int) -> bool:
        """Annule une demande en attente de l'employee connecté."""
        return user.annuler_demande(demande_id)

    # ------------------------------------------------------------------ #
    #  Statistiques                                                        #
    # ------------------------------------------------------------------ #

    @staticmethod
    def statistiques() -> dict:
        """
        Retourne un résumé global pour le tableau de bord manager.

        Exemple de retour :
        {
            "total_demandes": 10,
            "en_attente": 3,
            "approuvees": 5,
            "refusees": 2,
            "total_employees": 4
        }
        """
        demandes = Manager.charger_demandes()
        employees = Employee.charger_tous()

        stats = {
            "total_demandes": len(demandes),
            "en_attente":     sum(1 for d in demandes if d["status"] == "PENDING"),
            "approuvees":     sum(1 for d in demandes if d["status"] == "APPROVED"),
            "refusees":       sum(1 for d in demandes if d["status"] == "REJECTED"),
            "annulees":       sum(1 for d in demandes if d["status"] == "CANCELLED"),
            "total_employees": len(employees)
        }

        print(f"📊 Stats : {stats}")
        return stats

    @staticmethod
    def solde_employee(employee_id: int) -> int | None:
        """Retourne le solde de congés d'un employee par son ID."""
        employees = Employee.charger_tous()
        for u in employees:
            if u.id == employee_id:
                return u.vacation_balance
        return None

    @staticmethod
    def liste_employees() -> list[dict]:
        """Retourne la liste de tous les employees avec leur solde."""
        return [u.to_dict() for u in Employee.charger_tous()]