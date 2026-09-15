from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import MealLogCreate, MealLogRead, RecipeCheckRead, RecipeCreate, RecipeRead
from app.api.security import require_demo_api_key
from app.db.session import get_session
from app.services.meal_logging_service import MealLoggingService
from app.services.recipe_service import RecipeService

router = APIRouter(prefix="/households/{household_id}/recipes", tags=["recipes"])


def _schema_dump(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return value.dict()


@router.post("", response_model=RecipeRead, dependencies=[Depends(require_demo_api_key)])
def create_recipe(household_id: int, payload: RecipeCreate, session: Session = Depends(get_session)):
    return RecipeService(session).create_recipe(
        household_id=household_id,
        user_id=payload.user_id,
        name=payload.name,
        servings=payload.servings,
        instructions=payload.instructions,
        ingredients=[_schema_dump(ingredient) for ingredient in payload.ingredients],
    )


@router.get("/{recipe_id}/can-make", response_model=RecipeCheckRead)
def can_make_recipe(
    household_id: int,
    recipe_id: int,
    user_id: int,
    servings: int | None = None,
    session: Session = Depends(get_session),
):
    return RecipeService(session).check_can_make(household_id, user_id, recipe_id, servings)


@router.post("/{recipe_id}/meal-logs", response_model=MealLogRead, dependencies=[Depends(require_demo_api_key)])
def log_meal(household_id: int, recipe_id: int, payload: MealLogCreate, session: Session = Depends(get_session)):
    return MealLoggingService(session).log_recipe_meal(
        household_id=household_id,
        user_id=payload.user_id,
        recipe_id=recipe_id,
        servings=payload.servings,
        notes=payload.notes,
    )
