from datetime import date

from sqlalchemy import select

from app.db.models import InventoryTransaction
from app.domain.enums import TransactionType, Visibility
from app.services.household_service import HouseholdService
from app.services.inventory_service import InventoryService


def test_add_inventory_creates_transaction(session):
    household_service = HouseholdService(session)
    user = household_service.create_user("Alex")
    household = household_service.create_household("Home", user.id)

    InventoryService(session).add_manual_item(
        household.id,
        user.id,
        "eggs",
        6,
        "piece",
        Visibility.SHARED,
        date(2026, 1, 1),
    )

    transaction = session.scalar(select(InventoryTransaction))
    assert transaction is not None
    assert transaction.transaction_type == TransactionType.ADD
    assert transaction.quantity_delta == 6
