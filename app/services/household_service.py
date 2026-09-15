from sqlalchemy.orm import Session

from app.db.models import Household, User
from app.db.repositories.household_repository import HouseholdRepository
from app.db.repositories.user_repository import UserRepository
from app.utils.errors import NotFoundError


class HouseholdService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.households = HouseholdRepository(session)

    def create_user(self, display_name: str, telegram_id: int | None = None) -> User:
        user = self.users.create(display_name=display_name, telegram_id=telegram_id)
        self.session.commit()
        return user

    def get_or_create_telegram_user(self, telegram_id: int, display_name: str) -> User:
        user = self.users.get_by_telegram_id(telegram_id)
        if user:
            return user
        user = self.users.create(display_name=display_name or f"telegram-{telegram_id}", telegram_id=telegram_id)
        self.session.commit()
        return user

    def create_household(self, name: str, owner_user_id: int) -> Household:
        if not self.users.get(owner_user_id):
            raise NotFoundError("User not found")
        household = self.households.create(name=name)
        self.households.add_member(household.id, owner_user_id, role="owner")
        self.session.commit()
        return household

    def get_or_create_default_household(self, user_id: int, name: str = "My Kitchen") -> Household:
        households = self.households.list_for_user(user_id)
        if households:
            return households[0]
        return self.create_household(name, user_id)

    def require_member(self, household_id: int, user_id: int) -> None:
        if not self.households.user_is_member(household_id, user_id):
            raise NotFoundError("Household not found for user")
