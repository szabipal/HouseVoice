from datetime import date

from app.domain.enums import Visibility
from app.services.household_service import HouseholdService
from app.services.inventory_service import InventoryService


def test_private_items_are_visible_only_to_owner(session):
    household_service = HouseholdService(session)
    owner = household_service.create_user("Owner")
    other = household_service.create_user("Other")
    household = household_service.create_household("Home", owner.id)
    household_service.households.add_member(household.id, other.id)
    session.commit()

    inventory = InventoryService(session)
    inventory.add_manual_item(
        household.id,
        owner.id,
        "private chocolate",
        1,
        "piece",
        Visibility.PRIVATE,
        date(2026, 1, 1),
    )
    inventory.add_manual_item(
        household.id,
        owner.id,
        "shared milk",
        1,
        "l",
        Visibility.SHARED,
        date(2026, 1, 1),
    )

    owner_names = {item.name for item in inventory.list_visible(household.id, owner.id)}
    other_names = {item.name for item in inventory.list_visible(household.id, other.id)}

    assert owner_names == {"private chocolate", "shared milk"}
    assert other_names == {"shared milk"}
