import pytest

from app.engines.curtain_math import fabric_meters, split_panels

def test_living_room():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    assert r["panels"] == 5
    assert r["cut_height"] == 2.85
    assert r["meters"] == 14.25

def test_single_panel_narrow():
    r = fabric_meters(1.0, 2.0, 1.5, 0.0, 0.0, 2.8)
    assert r["panels"] == 1
    assert r["meters"] == 2.0

def test_default_ratio_even_split():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    assert r["left_panels"] == 2
    assert r["right_panels"] == 3
    assert r["left_ratio"] == 0.5
    # 总米数仍按总幅数计算
    assert r["meters"] == round(r["panels"] * r["cut_height"], 2)

def test_split_floors_left_remainder_right():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, left_ratio=0.2)
    assert r["panels"] == 5
    assert r["left_panels"] == 1      # floor(5 * 0.2)
    assert r["right_panels"] == 4
    assert r["meters"] == 14.25       # 不随分幅变化

def test_split_boundaries_zero_and_one():
    r0 = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, left_ratio=0.0)
    assert (r0["left_panels"], r0["right_panels"]) == (0, 5)
    r1 = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, left_ratio=1.0)
    assert (r1["left_panels"], r1["right_panels"]) == (5, 0)

def test_split_panels_unit():
    assert split_panels(5, 0.5) == (2, 3)
    assert split_panels(4, 0.5) == (2, 2)
    assert split_panels(1, 0.99) == (0, 1)

@pytest.mark.parametrize("ratio", [-0.01, 1.01, float("nan"), float("inf")])
def test_ratio_outside_closed_interval_rejected(ratio):
    with pytest.raises(ValueError):
        split_panels(5, ratio)
    with pytest.raises(ValueError):
        fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, left_ratio=ratio)

def test_zero_panels_rejected():
    with pytest.raises(ValueError):
        split_panels(0, 0.5)
