import base64
import json

from openai import OpenAI

from app.config import get_settings
from app.llm.schemas import ParsedRecipe, ReceiptExtractionResult
from app.llm.validators import validate_recipe_payload, validate_receipt_payload
from app.llm.prompts.receipt_extraction import PROMPT


class LLMClient:
    """LLM interface.

    Text-based methods remain deterministic placeholders. Image receipt
    extraction can use OpenAI vision when an API key is configured.
    """

    def extract_receipt_items(self, receipt_text: str) -> ReceiptExtractionResult:
        lines = [line.strip() for line in receipt_text.splitlines() if line.strip()]
        items = [{"name": line, "quantity": 1, "unit": "piece"} for line in lines[:20]]
        return validate_receipt_payload({"items": items})

    def extract_receipt_items_from_image(self, image_bytes: bytes) -> ReceiptExtractionResult:
        settings = get_settings()
        if not settings.openai_api_key:
            return self.extract_receipt_items("milk\neggs\nbread")

        b64 = base64.b64encode(image_bytes).decode()
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": PROMPT,
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{b64}",
                        },
                    ],
                }
            ],
            max_output_tokens=800,
        )

        raw = response.output_text.strip()
        raw = raw.strip("```json").strip("```").strip()
        items = json.loads(raw)
        return validate_receipt_payload({"items": items})

    def parse_recipe(self, recipe_text: str) -> ParsedRecipe:
        return validate_recipe_payload({
            "name": recipe_text.strip() or "Untitled recipe",
            "servings": 1,
            "ingredients": [],
            "instructions": "",
        })

    def route_command(self, message: str) -> dict:
        normalized = message.lower()
        if "receipt" in normalized:
            return {"intent": "receipt", "args": {}}
        if "recipe" in normalized:
            return {"intent": "recipe", "args": {}}
        return {"intent": "unknown", "args": {}}
