"""Shape payloads for history open views (unequal pair panels)."""

from __future__ import annotations

from copy import deepcopy


def has_unequal(result: dict) -> bool:
    return result.get("left_ratio") is not None and (
        result.get("left_panels") is not None or result.get("right_panels") is not None
    )


def rebalance_half(panels: int) -> tuple[int, int]:
    """Rebalance to 50/50-ish: left = panels//2, right = remainder."""
    left = int(panels) // 2
    right = int(panels) - left
    return left, right


def rebalance_all_left(panels: int) -> tuple[int, int]:
    """Alternate rebalance: all panels on the left."""
    return int(panels), 0


def open_rebalance(result: dict, mode: str = "half") -> dict:
    """Keep left_ratio, but rebalance left_panels / right_panels."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if not has_unequal(out):
        return out
    panels = int(out.get("panels") or 0)
    if panels <= 0:
        return out
    if mode == "all_left":
        left, right = rebalance_all_left(panels)
    else:
        left, right = rebalance_half(panels)
    out["left_panels"] = left
    out["right_panels"] = right
    out["open_rebalanced"] = True
    out["list_left_ratio"] = out.get("left_ratio")
    # left_ratio stays so the UI still shows the intended占比.
    return out


def summarize_unequal(result: dict) -> dict:
    """Flat view of ratio / left / right for open consumers."""
    if not isinstance(result, dict):
        return {}
    return {
        "left_ratio": result.get("left_ratio"),
        "left_panels": result.get("left_panels"),
        "right_panels": result.get("right_panels"),
        "panels": result.get("panels"),
        "open_rebalanced": bool(result.get("open_rebalanced")),
    }
