from app.domain.enums import Unit


MASS_TO_GRAMS = {Unit.GRAM.value: 1.0, Unit.KILOGRAM.value: 1000.0}
VOLUME_TO_ML = {Unit.MILLILITER.value: 1.0, Unit.LITER.value: 1000.0}


def canonical_unit(unit: str) -> str:
    aliases = {
        "gram": "g",
        "grams": "g",
        "kg": "kg",
        "kilogram": "kg",
        "kilograms": "kg",
        "ml": "ml",
        "milliliter": "ml",
        "milliliters": "ml",
        "l": "l",
        "liter": "l",
        "liters": "l",
        "piece": "piece",
        "pieces": "piece",
        "pack": "pack",
        "packs": "pack",
    }
    return aliases.get(unit.strip().lower(), unit.strip().lower())


def convert_quantity(quantity: float, from_unit: str, to_unit: str) -> float:
    source = canonical_unit(from_unit)
    target = canonical_unit(to_unit)
    if source == target:
        return quantity
    if source in MASS_TO_GRAMS and target in MASS_TO_GRAMS:
        return quantity * MASS_TO_GRAMS[source] / MASS_TO_GRAMS[target]
    if source in VOLUME_TO_ML and target in VOLUME_TO_ML:
        return quantity * VOLUME_TO_ML[source] / VOLUME_TO_ML[target]
    raise ValueError(f"Cannot convert from {from_unit} to {to_unit}")
