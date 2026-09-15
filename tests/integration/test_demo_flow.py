from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import get_session
from app.main import app


def test_documented_demo_flow():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool, future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False, future=True)

    def session_override():
        with Session() as session:
            yield session

    app.dependency_overrides[get_session] = session_override
    client = TestClient(app)

    try:
        user = client.post("/users", json={"display_name": "Alex", "telegram_id": 1001}).json()
        household = client.post("/households", json={"name": "Home", "owner_user_id": user["id"]}).json()
        household_id = household["id"]

        client.post(
            f"/households/{household_id}/inventory",
            json={"user_id": user["id"], "name": "pasta", "quantity": 500, "unit": "g", "visibility": "shared"},
        )
        client.post(
            f"/households/{household_id}/inventory",
            json={"user_id": user["id"], "name": "chocolate", "quantity": 1, "unit": "piece", "visibility": "private"},
        )
        recipe = client.post(
            f"/households/{household_id}/recipes",
            json={
                "user_id": user["id"],
                "name": "Pasta",
                "servings": 2,
                "ingredients": [{"name": "pasta", "quantity": 200, "unit": "g"}],
            },
        ).json()

        can_make = client.get(f"/households/{household_id}/recipes/{recipe['id']}/can-make", params={"user_id": user["id"]})
        assert can_make.json() == {"can_make": True, "missing": []}

        meal = client.post(
            f"/households/{household_id}/recipes/{recipe['id']}/meal-logs",
            json={"user_id": user["id"], "recipe_id": recipe["id"], "servings": 2, "notes": "demo"},
        )
        assert meal.status_code == 200

        inventory = client.get(f"/households/{household_id}/inventory", params={"user_id": user["id"]}).json()
        assert {item["name"]: item["quantity"] for item in inventory} == {"pasta": 300, "chocolate": 1}
    finally:
        app.dependency_overrides.clear()
