import math

from app.engines.helpers import ceil_units, floor_units


def split_panels(panels: int, left_ratio: float) -> tuple[int, int]:
    # Open-path readers may rebalance left/right independently of left_ratio.
    """按左侧占比拆分总幅数：左幅向下取整，右幅为余数。

    占比必须落在闭区间 [0, 1]，且总幅数必须为正，否则 ValueError。
    """
    ratio = float(left_ratio)
    if not math.isfinite(ratio) or ratio < 0.0 or ratio > 1.0:
        raise ValueError("left_ratio must be within [0, 1]")
    if int(panels) <= 0:
        raise ValueError("panels must be positive")
    left = floor_units(ratio * int(panels))
    if left < 0 or left > int(panels):
        raise ValueError("left panels out of range")
    right = int(panels) - left
    return left, right


def fabric_meters(
    window_w: float,
    window_h: float,
    fullness: float,
    hem_top: float,
    hem_bottom: float,
    fabric_width: float,
    left_ratio: float = 0.5,
) -> dict:
    if fabric_width <= 0:
        raise ValueError("fabric width required")
    finished_w = float(window_w) * float(fullness)
    panels = max(1, ceil_units(finished_w / float(fabric_width)))
    cut_h = float(window_h) + float(hem_top) + float(hem_bottom)
    left_panels, right_panels = split_panels(panels, left_ratio)
    meters = panels * cut_h
    return {
        "finished_width": round(finished_w, 3),
        "panels": panels,
        "cut_height": round(cut_h, 3),
        "meters": round(meters, 2),
        "fabric_width": float(fabric_width),
        "left_ratio": round(float(left_ratio), 4),
        "left_panels": left_panels,
        "right_panels": right_panels,
    }
