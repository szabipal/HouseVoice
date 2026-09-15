import re
from dataclasses import dataclass
from datetime import date

from sqlalchemy.orm import Session

from app.domain.enums import Visibility
from app.services.inventory_service import InventoryService


@dataclass(frozen=True)
class ParsedInventoryCommand:
    action: str
    name: str = ""
    quantity: float = 1.0
    unit: str = "piece"
    visibility: Visibility = Visibility.SHARED


def parse_inventory_command(text: str) -> ParsedInventoryCommand | None:
    """Parse deterministic inventory commands.

    Supported:
    - add milk 1 l shared
    - add chocolate 1 piece private
    - show inventory
    """
    normalized = text.strip().lower()
    if normalized in {"show inventory", "inventory", "show groceries", "my inventory"}:
        return ParsedInventoryCommand(action="list")

    match = re.match(
        r"^add\s+(?P<name>.+?)\s+(?P<quantity>\d+(?:\.\d+)?)\s+(?P<unit>[a-zA-Z]+)(?:\s+(?P<visibility>shared|private))?$",
        text.strip(),
        re.IGNORECASE,
    )
    if not match:
        return None

    visibility_text = (match.group("visibility") or Visibility.SHARED.value).lower()
    return ParsedInventoryCommand(
        action="add",
        name=match.group("name").strip(),
        quantity=float(match.group("quantity")),
        unit=match.group("unit").strip().lower(),
        visibility=Visibility(visibility_text),
    )


class InventoryHandler:
    def __init__(self, session: Session) -> None:
        self.session = session

    def handle(self, text: str, household_id: int, user_id: int) -> str | None:
        command = parse_inventory_command(text)
        if not command:
            return None

        service = InventoryService(self.session)
        if command.action == "list":
            items = service.list_visible(household_id, user_id)
            if not items:
                return "Your kitchen inventory is empty."
            lines = ["Visible inventory:"]
            for item in items:
                visibility = "private" if item.visibility == Visibility.PRIVATE else "shared"
                expiry = f", expires {item.expiry_date.isoformat()}" if item.expiry_date else ""
                lines.append(f"- {item.name}: {item.quantity:g} {item.unit} ({visibility}{expiry})")
            return "\n".join(lines)

        item = service.add_manual_item(
            household_id=household_id,
            user_id=user_id,
            name=command.name,
            quantity=command.quantity,
            unit=command.unit,
            visibility=command.visibility,
            purchase_date=date.today(),
        )
        return f"Added {item.name}: {item.quantity:g} {item.unit} ({item.visibility.value})."
