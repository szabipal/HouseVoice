from fastapi import APIRouter

router = APIRouter(prefix="/households/{household_id}/shopping-lists", tags=["shopping-lists"])


@router.get("")
def list_shopping_lists(household_id: int) -> list[dict]:
    return []
