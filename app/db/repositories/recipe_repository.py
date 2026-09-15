from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Recipe, RecipeIngredient


class RecipeRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, recipe: Recipe, ingredients: list[RecipeIngredient]) -> Recipe:
        recipe.ingredients = ingredients
        self.session.add(recipe)
        self.session.flush()
        return recipe

    def get(self, recipe_id: int) -> Recipe | None:
        stmt = select(Recipe).options(selectinload(Recipe.ingredients)).where(Recipe.id == recipe_id)
        return self.session.scalar(stmt)

    def list_for_household(self, household_id: int) -> list[Recipe]:
        stmt = select(Recipe).options(selectinload(Recipe.ingredients)).where(Recipe.household_id == household_id)
        return list(self.session.scalars(stmt).all())
