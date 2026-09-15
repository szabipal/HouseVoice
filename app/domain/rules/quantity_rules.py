from app.utils.units import convert_quantity


def scale_quantity(quantity: float, base_servings: int, target_servings: int) -> float:
    if base_servings <= 0 or target_servings <= 0:
        raise ValueError("Servings must be positive")
    return quantity * target_servings / base_servings


def has_enough(available_quantity: float, available_unit: str, required_quantity: float, required_unit: str) -> bool:
    converted_required = convert_quantity(required_quantity, required_unit, available_unit)
    return available_quantity + 1e-9 >= converted_required
