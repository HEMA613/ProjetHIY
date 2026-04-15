try:
    from .manager import Manager
    from .Utilisateur import Employee
except ImportError:
    from manager import Manager
    from Utilisateur import Employee


def authenticate(email: str, password: str):
    # Vérifier manager
    manager = Manager.login(email, password)
    if manager:
        return "manager", manager

    # Vérifier employee
    emp = Employee.login(email, password)
    if emp:
        return "employee", emp

    return None, None
