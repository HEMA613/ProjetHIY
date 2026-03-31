from datetime import date

class VacationService:

    @staticmethod
    def validate_dates(start_date: date, end_date: date):
        if start_date > end_date:
            raise ValueError("Dates invalides")

    @staticmethod
    def calculate_days(start_date: date, end_date: date):
        return (end_date - start_date).days + 1

    @staticmethod
    def has_enough_balance(balance: int, requested_days: int):
        return balance >= requested_days