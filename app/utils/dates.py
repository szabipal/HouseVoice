from datetime import date, timedelta


def today() -> date:
    return date.today()


def days_from_now(days: int) -> date:
    return today() + timedelta(days=days)
