from dataclasses import dataclass

@dataclass
class Employee:
    id: int
    name: str
    email: str
    role: str
    vacation_balance: int