import json, os
from datetime import date

class VacationService:
    def __init__(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        backend_data = os.path.join(project_root, "backend", "data")

        self.requests_file = os.path.join(backend_data, "demandes.json")
        self.employees_file = os.path.join(backend_data, "employes.json")
        self.manager_file = os.path.join(backend_data, "manager.json")

    def _load_json(self, path):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_json(self, path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_users(self):
        employees = self._load_json(self.employees_file)
        managers = self._load_json(self.manager_file)

        users = []
        for m in managers:
            users.append({
                "username": m.get("email"),
                "password": m.get("password"),
                "full_name": m.get("name"),
                "role": "manager",
                "total_days": 9999,
            })
        for e in employees:
            users.append({
                "username": e.get("email"),
                "password": e.get("password"),
                "full_name": e.get("name"),
                "role": "employee",
                "total_days": e.get("vacation_balance", 25),
            })
        return users

    def get_all_vacations(self):
        return self._load_json(self.requests_file)

    def get_user_vacations(self, username):
        user = next((u for u in self.load_users() if u["username"] == username), None)
        if not user:
            return []
        # Identifie par l'email (username)
        return [v for v in self.get_all_vacations()
                if v.get("employee_email") == username or v.get("employee_name") == user.get("full_name")]

    @staticmethod
    def _day_count(start_date, end_date):
        try:
            s = date.fromisoformat(start_date)
            e = date.fromisoformat(end_date)
            return (e - s).days + 1
        except Exception:
            return 0

    def get_used_days(self, username):
        vacs = self.get_user_vacations(username)
        return sum(self._day_count(v.get("start_date", ""), v.get("end_date", ""))
                   for v in vacs if v.get("status") in ("approved", "pending"))

    def get_remaining_days(self, username, total):
        used = self.get_used_days(username)
        return max(0, total - used)

    def submit_request(self, username, start_date, end_date, reason=""):
        demandes = self.get_all_vacations()
        next_id = max((d.get("id", 0) for d in demandes), default=0) + 1

        user = next((u for u in self.load_users() if u["username"] == username), None)
        if not user:
            raise ValueError("Utilisateur introuvable")

        new_req = {
            "id": next_id,
            "employee_id": None,
            "employee_email": username,
            "employee_name": user.get("full_name"),
            "start_date": start_date,
            "end_date": end_date,
            "days": self._day_count(start_date, end_date),
            "reason": reason,
            "status": "pending",
            "submitted_date": date.today().isoformat()
        }

        demandes.append(new_req)
        self._save_json(self.requests_file, demandes)
        return new_req

    def update_status(self, request_id, status):
        demandes = self.get_all_vacations()
        updated = False
        for d in demandes:
            if d.get("id") == request_id:
                d["status"] = status
                updated = True
        if updated:
            self._save_json(self.requests_file, demandes)
        return updated

