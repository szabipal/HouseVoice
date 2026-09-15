from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import HouseholdCreate, HouseholdRead, UserCreate, UserRead
from app.api.security import require_demo_api_key
from app.db.session import get_session
from app.services.household_service import HouseholdService

router = APIRouter(tags=["households"])


@router.post("/users", response_model=UserRead, dependencies=[Depends(require_demo_api_key)])
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    return HouseholdService(session).create_user(payload.display_name, payload.telegram_id)


@router.post("/households", response_model=HouseholdRead, dependencies=[Depends(require_demo_api_key)])
def create_household(payload: HouseholdCreate, session: Session = Depends(get_session)):
    return HouseholdService(session).create_household(payload.name, payload.owner_user_id)
