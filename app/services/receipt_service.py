from datetime import date

from sqlalchemy.orm import Session

from app.domain.enums import Visibility
from app.llm.client import LLMClient
from app.services.inventory_service import InventoryService
from app.vision.ocr import OCRClient


class ReceiptService:
    """Workflow service for receipt images."""

    def __init__(self, session: Session, ocr: OCRClient | None = None, llm: LLMClient | None = None) -> None:
        self.inventory = InventoryService(session)
        self.ocr = ocr or OCRClient()
        self.llm = llm or LLMClient()

    def ingest_receipt_image(self, household_id: int, user_id: int, image_bytes: bytes) -> list:
        extracted = self.llm.extract_receipt_items_from_image(image_bytes)
        added = []
        for item in extracted.items:
            added.append(
                self.inventory.add_manual_item(
                    household_id=household_id,
                    user_id=user_id,
                    name=item.name,
                    quantity=item.quantity,
                    unit=item.unit,
                    visibility=Visibility.SHARED,
                    purchase_date=date.today(),
                    expiry_date=item.expiry_date,
                )
            )
        return added
