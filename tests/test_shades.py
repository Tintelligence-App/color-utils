"""Tests for shade helpers in color_utils.shades."""

from importlib import import_module

cu = import_module("color_utils")


def test_get_darker_shades_length_and_format():
    """get_darker_shades should return the requested number of 7-char hex strings."""
    shades = cu.get_darker_shades("#FF0000", steps=3)
    assert isinstance(shades, tuple) and len(shades) == 3
    for s in shades:
        assert isinstance(s, str) and s.startswith("#") and len(s) == 7
