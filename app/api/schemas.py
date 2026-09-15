from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import TransactionType, Visibility


class UserCreate(BaseModel):
    display_name: str
    telegram_id: int | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    display_name: str
    telegram_id: int | None = None


class HouseholdCreate(BaseModel):
    name: str
    owner_user_id: int


class HouseholdRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class InventoryItemCreate(BaseModel):
    user_id: int
    name: str
    quantity: float = Field(gt=0)
    unit: str = "piece"
    visibility: Visibility = Visibility.SHARED
    purchase_date: date | None = None
    expiry_date: date | None = None
    low_stock_threshold: float | None = None


class InventoryItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    household_id: int
    owner_user_id: int
    name: str
    quantity: float
    unit: str
    visibility: Visibility
    expiry_date: date | None


class InventoryTransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    inventory_item_id: int
    user_id: int
    transaction_type: TransactionType
    quantity_delta: float
    unit: str
    reason: str
    created_at: datetime


class RecipeIngredientCreate(BaseModel):
    name: str
    quantity: float = Field(gt=0)
    unit: str = "piece"


class RecipeCreate(BaseModel):
    user_id: int
    name: str
    servings: int = Field(default=1, gt=0)
    instructions: str = ""
    ingredients: list[RecipeIngredientCreate]


class RecipeIngredientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    quantity: float
    unit: str


class RecipeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    household_id: int
    owner_user_id: int
    name: str
    servings: int
    instructions: str
    ingredients: list[RecipeIngredientRead] = []


class RecipeCheckRead(BaseModel):
    can_make: bool
    missing: list[str]


class MealLogCreate(BaseModel):
    user_id: int
    recipe_id: int
    servings: int = Field(default=1, gt=0)
    notes: str = ""


class MealLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    household_id: int
    recipe_id: int | None
    user_id: int
    servings: int
    notes: str
