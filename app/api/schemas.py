from datetime import date, datetime

from pydantic import BaseModel, Field

from app.domain.enums import TransactionType, Visibility


class UserCreate(BaseModel):
    display_name: str
    telegram_id: int | None = None


class UserRead(BaseModel):
    id: int
    display_name: str
    telegram_id: int | None = None

    class Config:
        orm_mode = True


class HouseholdCreate(BaseModel):
    name: str
    owner_user_id: int


class HouseholdRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


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
    id: int
    household_id: int
    owner_user_id: int
    name: str
    quantity: float
    unit: str
    visibility: Visibility
    expiry_date: date | None

    class Config:
        orm_mode = True


class InventoryTransactionRead(BaseModel):
    id: int
    inventory_item_id: int
    user_id: int
    transaction_type: TransactionType
    quantity_delta: float
    unit: str
    reason: str
    created_at: datetime

    class Config:
        orm_mode = True


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
    id: int
    name: str
    quantity: float
    unit: str

    class Config:
        orm_mode = True


class RecipeRead(BaseModel):
    id: int
    household_id: int
    owner_user_id: int
    name: str
    servings: int
    instructions: str
    ingredients: list[RecipeIngredientRead] = []

    class Config:
        orm_mode = True


class RecipeCheckRead(BaseModel):
    can_make: bool
    missing: list[str]


class MealLogCreate(BaseModel):
    user_id: int
    recipe_id: int
    servings: int = Field(default=1, gt=0)
    notes: str = ""


class MealLogRead(BaseModel):
    id: int
    household_id: int
    recipe_id: int | None
    user_id: int
    servings: int
    notes: str

    class Config:
        orm_mode = True
