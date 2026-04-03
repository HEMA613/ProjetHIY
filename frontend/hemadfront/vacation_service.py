import json, os
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


class VacationService:
    def __init__(self):
        self.vac_file   = os.path.join(DATA_DIR, "vacations.json")
        self.users_file = os.path.join(DATA_DIR, "users.json")

    # ── users ──────────────────────────────────────────────────
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, encoding="utf-8") as f:
                return json.load(f)
        return []

    # ── vacations ───────────────────────────────────────────────
    def load_vacations(self):
        if os.path.exists(self.vac_file):
            with open(self.vac_file, encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_vacations(self, data):
        with open(self.vac_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_user_vacations(self, username):
        return [v for v in self.load_vacations() if v["username"] == username]

    def get_all_vacations(self):
        return self.load_vacations()

    # ── days ────────────────────────────────────────────────────
    @staticmethod
    def count_days(start_str, end_str):
        try:
            s = date.fromisoformat(start_str)
            e = date.fromisoformat(end_str)
            return max(0, (e - s).days + 1)
        except Exception:
            return 0

    def get_used_days(self, username):
        return sum(
            self.count_days(v["start_date"], v["end_date"])
            for v in self.get_user_vacations(username)
            if v["status"] == "approved"
        )

    def get_remaining_days(self, username, total=25):
        return total - self.get_used_days(username)

    # ── CRUD ────────────────────────────────────────────────────
    def submit_request(self, username, start_date, end_date, reason):
        vacations = self.load_vacations()
        new_id = max((v["id"] for v in vacations), default=0) + 1
        entry = {
            "id": new_id,
            "username": username,
            "start_date": start_date,
            "end_date": end_date,
            "reason": reason,
            "status": "pending",
            "submitted_date": date.today().isoformat()
        }
        vacations.append(entry)
        self.save_vacations(vacations)
        return entry

    def update_status(self, vac_id, status):
        vacations = self.load_vacations()
        for v in vacations:
            if v["id"] == vac_id:
                v["status"] = status
                break
        self.save_vacations(vacations)
