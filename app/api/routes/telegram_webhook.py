import logging

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.security import require_telegram_secret
from app.bot.handlers.message_handler import MessageHandler
from app.db.session import get_session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/webhook", dependencies=[Depends(require_telegram_secret)])
async def telegram_webhook(request: Request, session: Session = Depends(get_session)) -> dict[str, bool]:
    update = await request.json()
    message = update.get("message", {})
    logger.info(
        "Telegram webhook update received: update_id=%s message_keys=%s",
        update.get("update_id"),
        sorted(message.keys()),
    )
    try:
        MessageHandler(session).handle_update(update)
    except Exception:
        logger.exception("Telegram webhook update failed: update_id=%s", update.get("update_id"))
        raise
    return {"ok": True}
