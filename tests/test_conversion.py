"""Tests for color conversion utilities in color_utils.conversion."""

from importlib import import_module

cu = import_module("color_utils")


def approx_equal(a, b, tol=1e-6):
    """Return True if numbers a and b are within tol."""
    return abs(a - b) <= tol


def test_hex_to_rgb_valid_and_invalid():
    """Validate hex_to_rgb for correct values and error handling."""
    assert cu.hex_to_rgb("#000000") == (0.0, 0.0, 0.0)
    assert cu.hex_to_rgb("FFFFFF") == (1.0, 1.0, 1.0)
    try:
        cu.hex_to_rgb("GGGGGG")
        assert False, "expected ValueError"
    except ValueError:
        pass
    try:
        cu.hex_to_rgb("#123")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_hex_to_hsv_and_rgb_to_hex_midpoint():
    """Check HSV conversion, RGB-to-hex, and midpoint calculation."""
    h, s, v = cu.hex_to_hsv("#FF0000")
    assert 0.0 <= h <= 1.0 and approx_equal(s, 1.0) and approx_equal(v, 1.0)
    assert cu.rgb_to_hex(255, 0, 0) == "#FF0000"
    assert cu.hex_midpoint("#000000", "#FFFFFF") == "#7F7F7F"


def test_rgb_to_lab_and_lch_and_normalize():
    """Cover Lab conversion, normalization, and LCH transformation."""
    # rgb_to_lab expects normalized RGB (0-1), not integers (0-255)
    l, a, b = cu.rgb_to_lab(1.0, 1.0, 1.0)  # White in normalized format
    assert 90.0 <= l <= 100.01
    l2, _a, _b = cu.normalize_lab(l, a, b)
    assert 0.9 <= (l2 or 0.0) <= 1.01
    L, C, H = cu.lab_to_lch(l, a, b)
    assert approx_equal(L, l)
    assert C >= 0.0
    assert 0.0 <= H < 360.0


def test_rgb255_to_hsl_primary_colors():
    """Hue values for pure red, green, and blue should match expected degrees."""
    # Function is exported as rgb255_to_hsl_percent
    assert cu.rgb255_to_hsl_percent(255, 0, 0)[0] == 0
    assert cu.rgb255_to_hsl_percent(0, 255, 0)[0] in (120,)
    assert cu.rgb255_to_hsl_percent(0, 0, 255)[0] in (240,)


def test_brightness_from_hex_monotonic():
    """Brightness should be higher for white than for black."""
    dark = cu.brightness_from_hex("#000000")
    bright = cu.brightness_from_hex("#FFFFFF")
    assert dark is not None and bright is not None
    assert bright > dark
