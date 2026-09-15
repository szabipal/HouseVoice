from datetime import date

from app.domain.enums import Visibility
from app.services.household_service import HouseholdService
from app.services.inventory_service import InventoryService
from app.services.meal_logging_service import MealLoggingService
from app.services.recipe_service import RecipeService


def test_recipe_can_be_made_and_deducts_inventory(session):
    households = HouseholdService(session)
    user = households.create_user("Alex")
    household = households.create_household("Home", user.id)

    InventoryService(session).add_manual_item(
        household.id,
        user.id,
        "pasta",
        500,
        "g",
        Visibility.SHARED,
        date(2026, 1, 1),
    )
    recipe = RecipeService(session).create_recipe(
        household.id,
        user.id,
        "Pasta",
        2,
        "",
        [{"name": "pasta", "quantity": 200, "unit": "g"}],
    )

    check = RecipeService(session).check_can_make(household.id, user.id, recipe.id, servings=2)
    assert check == {"can_make": True, "missing": []}

    MealLoggingService(session).log_recipe_meal(household.id, user.id, recipe.id, servings=2)
    remaining = InventoryService(session).list_visible(household.id, user.id)[0]
    assert remaining.quantity == 300
