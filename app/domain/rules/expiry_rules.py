from datetime import date, timedelta


DEFAULT_SHELF_LIFE_DAYS = {
    "milk": 7,
    "yogurt": 10,
    "chicken": 2,
    "beef": 3,
    "fish": 1,
    "eggs": 21,
    "bread": 5,
    "banana": 5,
    "lettuce": 4,
    "tomato": 7,
    "pasta": 365,
    "rice": 365,
}


def estimate_expiry_date(name: str, purchase_date: date) -> date:
    normalized = name.lower()
    days = 14
    for keyword, shelf_life in DEFAULT_SHELF_LIFE_DAYS.items():
        if keyword in normalized:
            days = shelf_life
            break
    return purchase_date + timedelta(days=days)


def is_expiring_soon(expiry_date: date | None, reference_date: date, window_days: int = 3) -> bool:
    if expiry_date is None:
        return False
    return reference_date <= expiry_date <= reference_date + timedelta(days=window_days)
