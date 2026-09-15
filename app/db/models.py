from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.domain.enums import TransactionType, Visibility


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=True)
    display_name = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    memberships = relationship("HouseholdMembership", back_populates="user")


class Household(Base):
    __tablename__ = "households"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    memberships = relationship("HouseholdMembership", back_populates="household")


class HouseholdMembership(Base):
    __tablename__ = "household_memberships"
    __table_args__ = (UniqueConstraint("household_id", "user_id", name="uq_household_user"),)

    id = Column(Integer, primary_key=True)
    household_id = Column(ForeignKey("households.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    role = Column(String(40), default="member", nullable=False)

    household = relationship("Household", back_populates="memberships")
    user = relationship("User", back_populates="memberships")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True)
    household_id = Column(ForeignKey("households.id"), nullable=False)
    owner_user_id = Column(ForeignKey("users.id"), nullable=False)
    name = Column(String(160), nullable=False)
    normalized_name = Column(String(160), nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    unit = Column(String(30), nullable=False)
    visibility = Column(Enum(Visibility), nullable=False)
    purchase_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    low_stock_threshold = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True)
    inventory_item_id = Column(ForeignKey("inventory_items.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity_delta = Column(Float, nullable=False)
    unit = Column(String(30), nullable=False)
    reason = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    household_id = Column(ForeignKey("households.id"), nullable=False)
    owner_user_id = Column(ForeignKey("users.id"), nullable=False)
    name = Column(String(160), nullable=False)
    instructions = Column(Text, default="", nullable=False)
    servings = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True)
    recipe_id = Column(ForeignKey("recipes.id"), nullable=False)
    name = Column(String(160), nullable=False)
    normalized_name = Column(String(160), nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    unit = Column(String(30), nullable=False)

    recipe = relationship("Recipe", back_populates="ingredients")


class MealLog(Base):
    __tablename__ = "meal_logs"

    id = Column(Integer, primary_key=True)
    household_id = Column(ForeignKey("households.id"), nullable=False)
    recipe_id = Column(ForeignKey("recipes.id"), nullable=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    servings = Column(Integer, nullable=False)
    notes = Column(Text, default="", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id = Column(Integer, primary_key=True)
    household_id = Column(ForeignKey("households.id"), nullable=False)
    name = Column(String(160), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ShoppingListItem(Base):
    __tablename__ = "shopping_list_items"

    id = Column(Integer, primary_key=True)
    shopping_list_id = Column(ForeignKey("shopping_lists.id"), nullable=False)
    name = Column(String(160), nullable=False)
    quantity = Column(Float, nullable=True)
    unit = Column(String(30), nullable=True)
    checked = Column(Boolean, default=False, nullable=False)
