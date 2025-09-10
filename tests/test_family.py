"""Tests for color family assignment in color_utils.family."""

from importlib import import_module

cu = import_module("color_utils")


def test_get_color_family_basic_cases():
    """Exercise core buckets: black/white/grey and several hue region checks."""
    # near black/white/grey
    assert cu.get_color_family(0.5, 0.0, 0.1) == "Black"
    assert cu.get_color_family(0.5, 0.1, 0.95) == "White / Off-white"
    assert cu.get_color_family(0.5, 0.1, 0.5) == "Grey"

    # hue mapping sanity checks
    assert cu.get_color_family(0.0, 1.0, 1.0) == "Red"
    assert cu.get_color_family(0.08, 1.0, 1.0) in ("Pink", "Orange")
    assert cu.get_color_family(0.16, 1.0, 1.0) == "Yellow"
    assert cu.get_color_family(0.3, 1.0, 1.0) == "Green"
    assert cu.get_color_family(0.52, 1.0, 1.0) == "Turquoise / Teal"
