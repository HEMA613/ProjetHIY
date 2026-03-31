from dataclasses import dataclass
from datetime import date

@dataclass
class VacationRequest:
    id: int
    employee_id: int
    start_date: date
    end_date: date
    days: int
    status: str
    reason: str