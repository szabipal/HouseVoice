from app.domain.rules.quantity_rules import has_enough, scale_quantity
from app.utils.units import convert_quantity


def test_quantity_conversion_mass():
    assert convert_quantity(1, "kg", "g") == 1000


def test_recipe_scaling():
    assert scale_quantity(200, base_servings=2, target_servings=3) == 300


def test_has_enough_with_conversion():
    assert has_enough(1, "kg", 500, "g")
    assert not has_enough(250, "g", 1, "kg")
