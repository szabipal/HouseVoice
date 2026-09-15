from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models import InventoryItem, InventoryTransaction
from app.domain.enums import TransactionType, Visibility


class InventoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_item(self, item: InventoryItem) -> InventoryItem:
        self.session.add(item)
        self.session.flush()
        return item

    def get(self, item_id: int) -> InventoryItem | None:
        return self.session.get(InventoryItem, item_id)

    def list_visible(self, household_id: int, user_id: int) -> list[InventoryItem]:
        stmt = (
            select(InventoryItem)
            .where(InventoryItem.household_id == household_id)
            .where(or_(InventoryItem.visibility == Visibility.SHARED, InventoryItem.owner_user_id == user_id))
            .order_by(InventoryItem.expiry_date.is_(None), InventoryItem.expiry_date, InventoryItem.name)
        )
        return list(self.session.scalars(stmt).all())

    def create_transaction(
        self,
        item_id: int,
        user_id: int,
        transaction_type: TransactionType,
        quantity_delta: float,
        unit: str,
        reason: str,
    ) -> InventoryTransaction:
        transaction = InventoryTransaction(
            inventory_item_id=item_id,
            user_id=user_id,
            transaction_type=transaction_type,
            quantity_delta=quantity_delta,
            unit=unit,
            reason=reason,
        )
        self.session.add(transaction)
        self.session.flush()
        return transaction
