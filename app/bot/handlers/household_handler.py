from sqlalchemy.orm import Session


class HouseholdHandler:
    def __init__(self, session: Session) -> None:
        self.session = session
