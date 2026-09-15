from datetime import date

from pydantic import BaseModel, Field


class ExtractedReceiptItem(BaseModel):
    name: str
    quantity: float = Field(gt=0)
    unit: str = "piece"
    price: float | None = None
    expiry_date: date | None = None


class ReceiptExtractionResult(BaseModel):
    items: list[ExtractedReceiptItem]


class ParsedRecipeIngredient(BaseModel):
    name: str
    quantity: float = Field(gt=0)
    unit: str = "piece"


class ParsedRecipe(BaseModel):
    name: str
    servings: int = Field(gt=0)
    ingredients: list[ParsedRecipeIngredient]
    instructions: str = ""


class CommandRoute(BaseModel):
    intent: str
    args: dict = {}
