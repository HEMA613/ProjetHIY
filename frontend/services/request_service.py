from models.request import VacationRequest
from services.vacation_service import VacationService

class RequestService:
    def __init__(self):
        self.requests = []

    def submit_request(self, employee, request_id, start_date, end_date, reason):
        VacationService.validate_dates(start_date, end_date)

        days = VacationService.calculate_days(start_date, end_date)

        if not VacationService.has_enough_balance(employee.vacation_balance, days):
            raise ValueError("Solde insuffisant")

        request = VacationRequest(
            id=request_id,
            employee_id=employee.id,
            start_date=start_date,
            end_date=end_date,
            days=days,
            status="PENDING",
            reason=reason
        )

        self.requests.append(request)
        return request