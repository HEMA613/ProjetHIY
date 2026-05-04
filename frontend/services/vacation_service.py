import json
import os
from datetime import date


class VacationService:
    """
    Service de gestion des congés - couche intermédiaire entre UI et données.

    Cette classe centralise toutes les opérations CRUD sur les demandes de congés :
    - Chargement/sauvegarde des données JSON
    - Gestion des utilisateurs
    - Soumission et traitement des demandes
    - Calculs des jours utilisés/restant
    """

    def __init__(self):
        """
        Initialise les chemins vers les fichiers de données.

        Les chemins sont calculés relativement au projet pour garantir
        la portabilité peu importe où le script est lancé.
        """
        # Calcul du répertoire racine du projet (deux niveaux au-dessus)
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        backend_data = os.path.join(project_root, "backend", "data")

        # Définition des chemins vers les fichiers JSON de données
        self.requests_file = os.path.join(
            backend_data, "demandes.json"
        )  # Demandes de congés
        self.employees_file = os.path.join(
            backend_data, "employes.json"
        )  # Données employés
        self.manager_file = os.path.join(
            backend_data, "manager.json"
        )  # Données managers

    def _load_json(self, path):
        """
        Charge un fichier JSON de manière sécurisée.

        Args:
            path: Chemin vers le fichier JSON

        Returns:
            list/dict: Contenu du fichier ou liste vide si inexistant
        """
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return []  # Retourne liste vide si fichier n'existe pas

    def _save_json(self, path, data):
        """
        Sauvegarde des données dans un fichier JSON.

        Args:
            path: Chemin du fichier de destination
            data: Données à sauvegarder (list/dict)
        """
        # Crée les répertoires parents si nécessaire
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            # Sauvegarde avec indentation et sans escaping ASCII
            # (pour caractères spéciaux)
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_users(self):
        """
        Charge et unifie tous les utilisateurs (managers + employés).

        Returns:
            list: Liste de dicts avec username, password, full_name, role, total_days
        """
        employees = self._load_json(self.employees_file)  # Chargement des employés
        managers = self._load_json(self.manager_file)  # Chargement des managers

        users = []

        # Traitement des managers (congés illimités)
        for m in managers:
            users.append(
                {
                    "username": m.get("email"),  # Email comme identifiant unique
                    "password": m.get("password"),  # Mot de passe pour connexion
                    "full_name": m.get("name"),  # Nom complet pour affichage
                    "role": "manager",  # Rôle manager
                    "total_days": 9999,  # Congés illimités pour managers
                }
            )

        # Traitement des employés (congés limités)
        for e in employees:
            users.append(
                {
                    "username": e.get("email"),  # Email comme identifiant unique
                    "password": e.get("password"),  # Mot de passe pour connexion
                    "full_name": e.get("name"),  # Nom complet pour affichage
                    "role": "employee",  # Rôle employé
                    "total_days": e.get(
                        "vacation_balance", 25
                    ),  # Solde limité (défaut 25j)
                }
            )

        return users

    def get_all_vacations(self):
        """
        Récupère toutes les demandes de congés avec normalisation des statuts.

        Returns:
            list: Liste des demandes avec statuts en minuscules
        """
        vacs = self._load_json(self.requests_file)
        # Normalisation des statuts (anciens fichiers peuvent avoir majuscules)
        for v in vacs:
            if isinstance(v.get("status"), str):
                v["status"] = v["status"].lower()
            # Ajoute "employee_email" si manquant mais que "employee_name" existe
            if "employee_email" not in v and "employee_name" in v:
                # Cherche l'email correspondant au nom
                for emp in self._load_json(self.employees_file):
                    if emp.get("name") == v.get("employee_name"):
                        v["employee_email"] = emp.get("email")
                        break
        return vacs

    def get_user_vacations(self, username):
        """
        Récupère les demandes d'un utilisateur spécifique.

        Args:
            username: Email de l'utilisateur

        Returns:
            list: Demandes filtrées pour cet utilisateur
        """
        user = next((u for u in self.load_users() if u["username"] == username), None)
        if not user:
            return []
        return [
            v
            for v in self.get_all_vacations()
            if v.get("employee_email") == username
            or v.get("employee_name") == user.get("full_name")
        ]

    @staticmethod
    def _day_count(start_date, end_date):
        """
        Calcule le nombre de jours entre deux dates (inclusif).

        Args:
            start_date: Date de début (string ISO format AAAA-MM-JJ)
            end_date: Date de fin (string ISO format AAAA-MM-JJ)

        Returns:
            int: Nombre de jours ou 0 en cas d'erreur de parsing
        """
        try:
            s = date.fromisoformat(start_date)  # Conversion string -> objet date
            e = date.fromisoformat(end_date)
            return (e - s).days + 1  # +1 car les dates sont inclusives
        except Exception:
            return 0  # Retourne 0 en cas d'erreur de format

    @staticmethod
    def count_days(start_date, end_date):
        """
        Wrapper public pour le calcul de jours.

        Args:
            start_date: Date de début
            end_date: Date de fin

        Returns:
            int: Nombre de jours
        """
        return VacationService._day_count(start_date, end_date)

    def get_used_days(self, username):
        """
        Calcule les jours de congés utilisés par un employé.

        Args:
            username: Email de l'utilisateur

        Returns:
            int: Nombre de jours utilisés (approuvés + en attente)
        """
        vacs = self.get_user_vacations(username)
        # Somme des jours pour statuts approuvés ou en attente
        return sum(
            self._day_count(v.get("start_date", ""), v.get("end_date", ""))
            for v in vacs
            if v.get("status") in ("approved", "pending")
        )

    def get_remaining_days(self, username, total):
        """
        Calcule les jours de congés restants.

        Args:
            username: Email de l'utilisateur
            total: Nombre total de jours disponibles

        Returns:
            int: Jours restants (minimum 0)
        """
        used = self.get_used_days(username)
        return max(0, total - used)  # Pas de valeur négative

    def submit_request(self, username, start_date, end_date, reason=""):
        """
        Soumet une nouvelle demande de congés.

        Args:
            username: Email du demandeur
            start_date: Date de début (ISO string)
            end_date: Date de fin (ISO string)
            reason: Motif optionnel

        Returns:
            dict: La demande créée

        Raises:
            ValueError: Si l'utilisateur n'existe pas
        """
        demandes = self.get_all_vacations()
        # Génération d'un nouvel ID unique (max existant + 1)
        next_id = max((d.get("id", 0) for d in demandes), default=0) + 1

        all_users = self.load_users()
        print(f"[DEBUG] username reçu: '{username}'")  # Debug temporaire
        print(
            f"[DEBUG] utilisateurs disponibles: {[u['username'] for u in all_users]}"
        )  # Debug temporaire

        user = next((u for u in all_users if u["username"] == username), None)
        if not user:
            raise ValueError("Utilisateur introuvable")

        new_req = {
            "id": next_id,
            "employee_id": None,  # Legacy, peut être retiré dans future version
            "employee_email": username,
            "employee_name": user.get("full_name"),
            "start_date": start_date,
            "end_date": end_date,
            "days": self._day_count(start_date, end_date),  # Calcul automatique
            "reason": reason,
            "status": "pending",  # Statut initial
            "submitted_date": date.today().isoformat(),  # Date de soumission
        }

        demandes.append(new_req)  # Ajout à la liste existante
        self._save_json(self.requests_file, demandes)  # Sauvegarde persistante
        return new_req

    def update_status(self, request_id, status):
        """
        Met à jour le statut d'une demande de congés.

        Args:
            request_id: ID de la demande à modifier
            status: Nouveau statut (approved/rejected/pending)

        Returns:
            bool: True si mise à jour réussie, False sinon
        """
        status = (
            status.lower() if isinstance(status, str) else status
        )  # Normalisation minuscule
        demandes = self.get_all_vacations()
        updated = False

        # Recherche et mise à jour de la demande spécifique
        for d in demandes:
            if d.get("id") == request_id:
                d["status"] = status
                updated = True
                break  # Sortie dès qu'on trouve (optimisation)

        if updated:
            self._save_json(self.requests_file, demandes)  # Sauvegarde si modifié

        return updated
