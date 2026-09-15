from app.llm.client import LLMClient
from app.vision.ocr import OCRClient


class ReceiptParser:
    def __init__(self, ocr: OCRClient | None = None, llm: LLMClient | None = None) -> None:
        self.ocr = ocr or OCRClient()
        self.llm = llm or LLMClient()

    def parse(self, image_bytes: bytes):
        return self.llm.extract_receipt_items(self.ocr.extract_text(image_bytes))
