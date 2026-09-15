from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.db.models import Household, HouseholdMembership


class HouseholdRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, name: str) -> Household:
        household = Household(name=name)
        self.session.add(household)
        self.session.flush()
        return household

    def add_member(self, household_id: int, user_id: int, role: str = "member") -> HouseholdMembership:
        membership = HouseholdMembership(household_id=household_id, user_id=user_id, role=role)
        self.session.add(membership)
        self.session.flush()
        return membership

    def get(self, household_id: int) -> Household | None:
        return self.session.get(Household, household_id)

    def list_for_user(self, user_id: int) -> list[Household]:
        stmt = (
            select(Household)
            .join(HouseholdMembership, HouseholdMembership.household_id == Household.id)
            .where(HouseholdMembership.user_id == user_id)
            .order_by(Household.id)
        )
        return list(self.session.scalars(stmt).all())

    def user_is_member(self, household_id: int, user_id: int) -> bool:
        stmt = select(exists().where(
            HouseholdMembership.household_id == household_id,
            HouseholdMembership.user_id == user_id,
        ))
        return bool(self.session.scalar(stmt))
