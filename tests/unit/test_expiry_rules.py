from datetime import date

from app.domain.rules.expiry_rules import estimate_expiry_date, is_expiring_soon


def test_estimates_known_shelf_life():
    assert estimate_expiry_date("whole milk", date(2026, 1, 1)) == date(2026, 1, 8)


def test_expiring_soon_window():
    assert is_expiring_soon(date(2026, 1, 4), date(2026, 1, 1), window_days=3)
    assert not is_expiring_soon(date(2026, 1, 5), date(2026, 1, 1), window_days=3)
