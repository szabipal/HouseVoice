from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import InventoryItemCreate, InventoryItemRead
from app.api.security import require_demo_api_key
from app.db.session import get_session
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/households/{household_id}/inventory", tags=["inventory"])


@router.post("", response_model=InventoryItemRead, dependencies=[Depends(require_demo_api_key)])
def add_inventory_item(household_id: int, payload: InventoryItemCreate, session: Session = Depends(get_session)):
    return InventoryService(session).add_manual_item(
        household_id=household_id,
        user_id=payload.user_id,
        name=payload.name,
        quantity=payload.quantity,
        unit=payload.unit,
        visibility=payload.visibility,
        purchase_date=payload.purchase_date or date.today(),
        expiry_date=payload.expiry_date,
        low_stock_threshold=payload.low_stock_threshold,
    )


@router.get("", response_model=list[InventoryItemRead])
def list_inventory(household_id: int, user_id: int, session: Session = Depends(get_session)):
    return InventoryService(session).list_visible(household_id, user_id)
