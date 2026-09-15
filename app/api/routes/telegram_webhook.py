from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.security import require_telegram_secret
from app.bot.handlers.message_handler import MessageHandler
from app.db.session import get_session

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/webhook", dependencies=[Depends(require_telegram_secret)])
async def telegram_webhook(request: Request, session: Session = Depends(get_session)) -> dict[str, bool]:
    update = await request.json()
    MessageHandler(session).handle_update(update)
    return {"ok": True}
