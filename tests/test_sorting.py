"""Tests for sorting helpers in color_utils.sorting."""

from importlib import import_module

cu = import_module("color_utils")


def test_sort_paints_by_color_modes():
    """sort_paints_by_color should accept hue/saturation/value and return list of same length."""
    paints = [
        {"name": "red", "color_primary": "#FF0000"},
        {"name": "green", "color_primary": "#00FF00"},
        {"name": "blue", "color_primary": "#0000FF"},
    ]
    for mode in ("hue", "saturation", "value"):
        sorted_list = cu.sort_paints_by_color(paints, mode)
        assert isinstance(sorted_list, list) and len(sorted_list) == 3


def test_sort_paints_by_family_value_hue_enrichment():
    """sort_paints_by_family_value_hue should enrich each item with _hsv and _family keys."""
    paints = [
        {"name": "r", "color_primary": "#FF0000"},
        {"name": "g", "color_primary": "#00FF00"},
        {"name": "b", "color_primary": "#0000FF"},
    ]
    out = cu.sort_paints_by_family_value_hue(paints)
    assert isinstance(out, list) and len(out) == 3
    assert all("_hsv" in p and "_family" in p for p in out)
