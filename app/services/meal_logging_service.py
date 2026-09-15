from sqlalchemy.orm import Session

from app.db.models import MealLog
from app.db.repositories.household_repository import HouseholdRepository
from app.db.repositories.inventory_repository import InventoryRepository
from app.db.repositories.meal_log_repository import MealLogRepository
from app.db.repositories.recipe_repository import RecipeRepository
from app.domain.enums import TransactionType
from app.domain.rules.inventory_rules import remaining_after_deduction
from app.domain.rules.quantity_rules import has_enough, scale_quantity
from app.utils.errors import InsufficientInventoryError, NotFoundError


class MealLoggingService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.households = HouseholdRepository(session)
        self.inventory = InventoryRepository(session)
        self.recipes = RecipeRepository(session)
        self.meal_logs = MealLogRepository(session)

    def log_recipe_meal(self, household_id: int, user_id: int, recipe_id: int, servings: int, notes: str = "") -> MealLog:
        if not self.households.user_is_member(household_id, user_id):
            raise NotFoundError("Household not found for user")
        recipe = self.recipes.get(recipe_id)
        if not recipe or recipe.household_id != household_id:
            raise NotFoundError("Recipe not found")

        visible_items = self.inventory.list_visible(household_id, user_id)
        deductions = []
        for ingredient in recipe.ingredients:
            required = scale_quantity(ingredient.quantity, recipe.servings, servings)
            match = next(
                (
                    item for item in visible_items
                    if item.normalized_name == ingredient.normalized_name
                    and has_enough(item.quantity, item.unit, required, ingredient.unit)
                ),
                None,
            )
            if not match:
                raise InsufficientInventoryError(f"Not enough {ingredient.name}")
            deductions.append((match, required, ingredient.unit))

        meal_log = self.meal_logs.create(
            MealLog(
                household_id=household_id,
                recipe_id=recipe_id,
                user_id=user_id,
                servings=servings,
                notes=notes,
            )
        )
        for item, quantity, unit in deductions:
            item.quantity = remaining_after_deduction(item, quantity, unit)
            self.inventory.create_transaction(
                item.id,
                user_id,
                TransactionType.DEDUCT,
                -quantity,
                unit,
                f"cooked recipe #{recipe_id}",
            )
        self.session.commit()
        return meal_log
