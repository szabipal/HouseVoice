from pydantic import ValidationError

from app.llm.schemas import CommandRoute, ParsedRecipe, ReceiptExtractionResult


def validate_receipt_payload(payload: dict) -> ReceiptExtractionResult:
    if hasattr(ReceiptExtractionResult, "model_validate"):
        return ReceiptExtractionResult.model_validate(payload)
    return ReceiptExtractionResult.parse_obj(payload)


def validate_recipe_payload(payload: dict) -> ParsedRecipe:
    if hasattr(ParsedRecipe, "model_validate"):
        return ParsedRecipe.model_validate(payload)
    return ParsedRecipe.parse_obj(payload)


def validate_command_payload(payload: dict) -> CommandRoute:
    try:
        if hasattr(CommandRoute, "model_validate"):
            return CommandRoute.model_validate(payload)
        return CommandRoute.parse_obj(payload)
    except ValidationError:
        return CommandRoute(intent="unknown", args={})
