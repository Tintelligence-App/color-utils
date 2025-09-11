"""Tests for sorting helpers in color_utils.sorting."""

from importlib import import_module

cu = import_module("color_utils")


def test_sort_paints_by_color_modes():
    """sort_paints_by_color should accept hue/saturation/value and return list of same length."""
    paints = [
        {"name": "red", "hsv_h": 0.0, "hsv_s": 1.0, "hsv_v": 1.0},
        {"name": "green", "hsv_h": 1 / 3, "hsv_s": 1.0, "hsv_v": 1.0},
        {"name": "blue", "hsv_h": 2 / 3, "hsv_s": 1.0, "hsv_v": 1.0},
    ]
    for mode in ("hue", "saturation", "value"):
        sorted_list = cu.sort_paints_by_color(paints, mode)
        assert isinstance(sorted_list, list) and len(sorted_list) == 3


def test_sort_paints_by_family_value_hue_order_param():
    """family-id grouping with value order parameter should work (bright vs dark)."""
    # assume family ids: Red=6, Green=5 (from color_families.json)
    paints = [
        {
            "name": "dim red",
            "color_family_id": 6,
            "hsv_h": 0.0,
            "hsv_s": 1.0,
            "hsv_v": 0.4,
        },
        {
            "name": "bright red",
            "color_family_id": 6,
            "hsv_h": 0.0,
            "hsv_s": 1.0,
            "hsv_v": 0.9,
        },
        {
            "name": "green",
            "color_family_id": 5,
            "hsv_h": 1 / 3,
            "hsv_s": 1.0,
            "hsv_v": 0.8,
        },
    ]
    out_bright = cu.sort_paints_by_family_value_hue(paints, order="bright_to_dark")
    assert [p["name"] for p in out_bright if p["color_family_id"] == 6][:2] == [
        "bright red",
        "dim red",
    ]
    out_dark = cu.sort_paints_by_family_value_hue(paints, order="dark_to_bright")
    assert [p["name"] for p in out_dark if p["color_family_id"] == 6][:2] == [
        "dim red",
        "bright red",
    ]


def test_sort_paints_by_family_lab_brightness_order_param():
    """family-id grouping with brightness order parameter should work (bright vs dark)."""
    # assume family ids: Red=6, Green=5 (from color_families.json)
    paints = [
        {"name": "dark red", "color_family_id": 6, "lab_l": 30.0, "hsv_h": 0.0},
        {"name": "bright red", "color_family_id": 6, "lab_l": 80.0, "hsv_h": 0.0},
        {"name": "green", "color_family_id": 5, "lab_l": 70.0, "hsv_h": 1 / 3},
    ]
    out_bright = cu.sort_paints_by_family_lab_brightness(paints, order="bright_to_dark")
    assert [p["name"] for p in out_bright if p["color_family_id"] == 6][:2] == [
        "bright red",
        "dark red",
    ]
    out_dark = cu.sort_paints_by_family_lab_brightness(paints, order="dark_to_bright")
    assert [p["name"] for p in out_dark if p["color_family_id"] == 6][:2] == [
        "dark red",
        "bright red",
    ]
