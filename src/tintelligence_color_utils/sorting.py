"""Utilities for sorting paint dictionaries by color properties or family."""

from __future__ import annotations

from typing import Dict, List, Literal

from .families import COLOR_FAMILY_ID_ORDER, COLOR_FAMILY_ID_TO_NAME


def sort_paints_by_color(paints: List[Dict], mode: str = "hue") -> List[Dict]:
    """Sort a list of paint dictionaries by color property (hue, saturation, or value)."""
    if mode not in {"hue", "saturation", "value"}:
        raise ValueError("mode must be 'hue', 'saturation', or 'value'")

    def get_sort_key(paint: Dict):
        h = paint.get("hsv_h")
        s = paint.get("hsv_s")
        v = paint.get("hsv_v")
        if h is None or s is None or v is None:
            raise KeyError("paint must contain 'hsv_h', 'hsv_s', 'hsv_v'")
        return {"hue": h, "saturation": s, "value": v}[mode]

    return sorted(paints, key=get_sort_key)


def sort_paints_by_family_value_hue(
    paints: List[Dict],
    order: Literal["bright_to_dark", "dark_to_bright"] = "bright_to_dark",
) -> List[Dict]:
    """Group by color family id (from JSON), then sort by HSV value and hue.

    - Primary grouping: `color_family_id` using `COLOR_FAMILY_ID_ORDER`
    - Secondary sort: HSV V (value) by `order`
    - Tertiary sort: HSV H (hue) ascending

    Expects paints to have `color_family_id`, `hsv_h`, `hsv_s`, `hsv_v`.
    Enriches each item with `_hsv` and `_family` for backward compatibility.
    """
    id_to_index = {fid: idx for idx, fid in enumerate(COLOR_FAMILY_ID_ORDER)}
    value_sign = -1 if order == "bright_to_dark" else 1

    enriched_paints: List[Dict] = []
    for paint in paints:
        fam_id = paint.get("color_family_id")
        h = paint.get("hsv_h")
        s = paint.get("hsv_s")
        v = paint.get("hsv_v")
        if fam_id is None:
            raise KeyError("paint must contain 'color_family_id'")
        if h is None or s is None or v is None:
            raise KeyError("paint must contain 'hsv_h', 'hsv_s', 'hsv_v'")
        family_name = COLOR_FAMILY_ID_TO_NAME.get(fam_id, "Unknown")
        enriched_paints.append({**paint, "_hsv": (h, s, v), "_family": family_name})

    def sort_key(p: Dict):
        fam_idx = id_to_index.get(p["color_family_id"], len(COLOR_FAMILY_ID_ORDER))
        return (
            fam_idx,
            value_sign * p["hsv_v"],
            p["hsv_h"],
        )

    return sorted(enriched_paints, key=sort_key)


def sort_paints_by_family_lab_brightness(
    paints: List[Dict],
    order: Literal["bright_to_dark", "dark_to_bright"] = "bright_to_dark",
) -> List[Dict]:
    """Group by color family id, then sort by Lab L within each family.

    - Primary grouping: `color_family_id` compared against COLOR_FAMILY_ID_ORDER
    - Secondary sort: Lab L (`lab_l`) in the specified order
    - Tertiary tie-breaker: hue (`hsv_h`) ascending if present, else 0

    Required fields: `color_family_id`, `lab_l`
    Optional: `hsv_h` (used only as stable tie-breaker)
    """
    enriched = []
    for paint in paints:
        fam_id = paint.get("color_family_id")
        l = paint.get("lab_l")
        if fam_id is None:
            raise KeyError("paint must contain 'color_family_id'")
        if l is None:
            raise KeyError("paint must contain 'lab_l'")
        enriched.append(paint)

    id_to_index = {fid: idx for idx, fid in enumerate(COLOR_FAMILY_ID_ORDER)}
    brightness_sign = -1 if order == "bright_to_dark" else 1

    def sort_key(p: Dict):
        fam_idx = id_to_index.get(p["color_family_id"], len(COLOR_FAMILY_ID_ORDER))
        hue = p.get("hsv_h") or 0.0
        return (
            fam_idx,
            brightness_sign * p["lab_l"],
            hue,
        )

    return sorted(enriched, key=sort_key)
