from sqlalchemy.orm import Session

from app.db.models import MealLog


class MealLogRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, meal_log: MealLog) -> MealLog:
        self.session.add(meal_log)
        self.session.flush()
        return meal_log
