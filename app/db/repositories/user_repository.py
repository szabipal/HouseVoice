from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, display_name: str, telegram_id: int | None = None) -> User:
        user = User(display_name=display_name, telegram_id=telegram_id)
        self.session.add(user)
        self.session.flush()
        return user

    def get(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return self.session.scalar(select(User).where(User.telegram_id == telegram_id))
