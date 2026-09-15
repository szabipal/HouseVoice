from app.db.models import InventoryItem
from app.domain.enums import Visibility
from app.utils.units import convert_quantity


def item_visible_to_user(item: InventoryItem, user_id: int) -> bool:
    return item.visibility == Visibility.SHARED or item.owner_user_id == user_id


def remaining_after_deduction(item: InventoryItem, quantity: float, unit: str) -> float:
    deduction = convert_quantity(quantity, unit, item.unit)
    return max(0.0, item.quantity - deduction)
