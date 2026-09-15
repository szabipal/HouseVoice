from sqlalchemy.orm import Session

from app.db.models import Recipe, RecipeIngredient
from app.db.repositories.household_repository import HouseholdRepository
from app.db.repositories.inventory_repository import InventoryRepository
from app.db.repositories.recipe_repository import RecipeRepository
from app.domain.rules.quantity_rules import has_enough, scale_quantity
from app.utils.errors import ForbiddenError, NotFoundError
from app.utils.text_normalization import normalize_food_name


class RecipeService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.households = HouseholdRepository(session)
        self.inventory = InventoryRepository(session)
        self.recipes = RecipeRepository(session)

    def create_recipe(
        self,
        household_id: int,
        user_id: int,
        name: str,
        servings: int,
        instructions: str,
        ingredients: list[dict],
    ) -> Recipe:
        if not self.households.user_is_member(household_id, user_id):
            raise ForbiddenError("User is not a household member")
        recipe = Recipe(
            household_id=household_id,
            owner_user_id=user_id,
            name=name,
            servings=servings,
            instructions=instructions,
        )
        ingredient_models = [
            RecipeIngredient(
                name=i["name"],
                normalized_name=normalize_food_name(i["name"]),
                quantity=float(i["quantity"]),
                unit=i["unit"],
            )
            for i in ingredients
        ]
        recipe = self.recipes.create(recipe, ingredient_models)
        self.session.commit()
        return recipe

    def check_can_make(self, household_id: int, user_id: int, recipe_id: int, servings: int | None = None) -> dict:
        if not self.households.user_is_member(household_id, user_id):
            raise NotFoundError("Household not found for user")
        recipe = self.recipes.get(recipe_id)
        if not recipe or recipe.household_id != household_id:
            raise NotFoundError("Recipe not found")
        target_servings = servings or recipe.servings
        visible_items = self.inventory.list_visible(household_id, user_id)
        missing: list[str] = []

        for ingredient in recipe.ingredients:
            required = scale_quantity(ingredient.quantity, recipe.servings, target_servings)
            matches = [i for i in visible_items if i.normalized_name == ingredient.normalized_name]
            if not any(has_enough(item.quantity, item.unit, required, ingredient.unit) for item in matches):
                missing.append(f"{ingredient.name}: {required:g} {ingredient.unit}")

        return {"can_make": not missing, "missing": missing}
