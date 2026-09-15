from fastapi import FastAPI

from app.api.routes import health, households, inventory, recipes, shopping_lists, telegram_webhook
from app.db.session import init_database


def create_app() -> FastAPI:
    app = FastAPI(title="Kitchen Household Assistant")
    app.include_router(health.router)
    app.include_router(households.router)
    app.include_router(inventory.router)
    app.include_router(recipes.router)
    app.include_router(shopping_lists.router)
    app.include_router(telegram_webhook.router)

    @app.on_event("startup")
    def startup() -> None:
        init_database()

    return app


app = create_app()
