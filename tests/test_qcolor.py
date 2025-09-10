"""Tests for Qt QColor helper using a dummy qt_core shim to avoid Qt dependency."""

import sys
import types
from importlib import import_module

# install a dummy qt_core with QColor for the duration of this test module
qt_core = types.ModuleType("qt_core")


class DummyQColor:
    """Minimal stand-in for a Qt QColor used for testing."""

    def __init__(self, *args):
        self.args = args


qt_core.QColor = DummyQColor  # type: ignore
sys.modules["qt_core"] = qt_core

cu_q = import_module("color_utils.qcolor")


def test_to_qcolor_with_dummy_qt_core():
    """to_qcolor should accept str, tuple, and QColor instance when QColor is available."""
    c1 = cu_q.to_qcolor("#FF0000")
    assert isinstance(c1, DummyQColor)
    c2 = cu_q.to_qcolor((255, 0, 0))
    assert isinstance(c2, DummyQColor)
    c3 = cu_q.to_qcolor(DummyQColor())
    assert isinstance(c3, DummyQColor)
