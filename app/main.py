from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.api.routes import health, households, inventory, recipes, shopping_lists, telegram_webhook
from app.db.session import init_database


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_database()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Kitchen Household Assistant", lifespan=lifespan)
    app.include_router(health.router)
    app.include_router(households.router)
    app.include_router(inventory.router)
    app.include_router(recipes.router)
    app.include_router(shopping_lists.router)
    app.include_router(telegram_webhook.router)

    return app


app = create_app()
