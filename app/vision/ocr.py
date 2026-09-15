class OCRClient:
    """Deterministic OCR placeholder.

    Tests and local development can pass UTF-8 text bytes to simulate OCR.
    """

    def extract_text(self, image_bytes: bytes) -> str:
        try:
            return image_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return "milk\neggs\nbread"
