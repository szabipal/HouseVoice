from sqlalchemy.orm import Session


class RecipeHandler:
    def __init__(self, session: Session) -> None:
        self.session = session

    def handle(self, message: dict) -> None:
        return None
