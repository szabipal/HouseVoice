from datetime import date

from sqlalchemy.orm import Session

from app.db.models import InventoryItem
from app.db.repositories.household_repository import HouseholdRepository
from app.db.repositories.inventory_repository import InventoryRepository
from app.domain.enums import TransactionType, Visibility
from app.domain.rules.expiry_rules import estimate_expiry_date
from app.utils.errors import ForbiddenError, NotFoundError
from app.utils.text_normalization import normalize_food_name


class InventoryService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.households = HouseholdRepository(session)
        self.inventory = InventoryRepository(session)

    def add_manual_item(
        self,
        household_id: int,
        user_id: int,
        name: str,
        quantity: float,
        unit: str,
        visibility: Visibility,
        purchase_date: date,
        expiry_date: date | None = None,
        low_stock_threshold: float | None = None,
    ) -> InventoryItem:
        if not self.households.user_is_member(household_id, user_id):
            raise ForbiddenError("User is not a household member")
        item = InventoryItem(
            household_id=household_id,
            owner_user_id=user_id,
            name=name,
            normalized_name=normalize_food_name(name),
            quantity=quantity,
            unit=unit,
            visibility=visibility,
            purchase_date=purchase_date,
            expiry_date=expiry_date or estimate_expiry_date(name, purchase_date),
            low_stock_threshold=low_stock_threshold,
        )
        self.inventory.add_item(item)
        self.inventory.create_transaction(
            item.id,
            user_id,
            TransactionType.ADD,
            quantity,
            unit,
            "manual inventory item",
        )
        self.session.commit()
        return item

    def list_visible(self, household_id: int, user_id: int) -> list[InventoryItem]:
        if not self.households.user_is_member(household_id, user_id):
            raise NotFoundError("Household not found for user")
        return self.inventory.list_visible(household_id, user_id)
