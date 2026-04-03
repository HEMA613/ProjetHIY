import json, os

class VacationService:
    def __init__(self):
        self.file = "data/vacations.json"

    def load(self):
        if os.path.exists(self.file):
            with open(self.file) as f:
                return json.load(f)
        return []

    def save(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)
