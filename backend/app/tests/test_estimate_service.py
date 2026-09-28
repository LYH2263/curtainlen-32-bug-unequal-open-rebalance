import pytest
from fastapi.testclient import TestClient

from app import db as db_module
from app import seed
from app.main import app
from app.repositories import history


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(db_module, "DB_PATH", tmp_path / "test.db")
    with TestClient(app) as c:
        yield c


def test_dry_calc_returns_split_without_history(client):
    before = len(history.list_runs())
    r = client.get("/api/estimate", params={"window_id": 1, "fabric_id": 1, "left_ratio": 0.3})
    assert r.status_code == 200
    data = r.json()
    assert data["run_id"] is None
    assert data["panels"] == 5
    assert data["left_panels"] == 1
    assert data["right_panels"] == 4
    assert data["meters"] == 14.25
    assert len(history.list_runs()) == before


def test_invalid_ratio_fails_and_writes_no_history(client):
    before = len(history.list_runs())
    r = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "save": True, "left_ratio": 1.2,
    })
    assert r.status_code == 422
    assert len(history.list_runs()) == before

    rq = client.get("/api/estimate", params={
        "window_id": 1, "fabric_id": 1, "save": True, "left_ratio": -0.1,
    })
    assert rq.status_code == 422
    assert len(history.list_runs()) == before


def test_saved_run_pins_split_and_lookup_by_id(client):
    r = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "save": True, "left_ratio": 0.3, "note": "左窄",
    })
    assert r.status_code == 200
    run_id = r.json()["run_id"]
    assert run_id is not None

    snap = client.get(f"/api/runs/{run_id}").json()
    res = snap["result"]
    assert res["left_ratio"] == 0.3
    assert res["left_panels"] == 1
    assert res["right_panels"] == 4
    assert res["panels"] == 5
    assert res["meters"] == 14.25
    assert snap["note"] == "左窄"


def test_changing_ratio_does_not_rewrite_old_run(client):
    first = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "save": True, "left_ratio": 0.3,
    }).json()
    first_id = first["run_id"]

    client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "save": True, "left_ratio": 0.8,
    })

    old = client.get(f"/api/runs/{first_id}").json()["result"]
    # 按编号回看仍是写入时的左右幅数
    assert old["left_ratio"] == 0.3
    assert old["left_panels"] == 1
    assert old["right_panels"] == 4


def test_window_runs_filter_latest_split(client):
    client.post("/api/estimate", json={"window_id": 1, "fabric_id": 1, "save": True, "left_ratio": 0.2})
    latest = client.get("/api/runs", params={"window_id": 1, "limit": 1}).json()["items"][0]["result"]
    assert latest["left_panels"] == 1
    assert latest["right_panels"] == 4


def test_list_readback_keeps_writetime_split_and_totals(client):
    client.post("/api/estimate", json={"window_id": 1, "fabric_id": 1, "save": True, "left_ratio": 0.8})
    item = client.get("/api/runs", params={"limit": 1}).json()["items"][0]
    res = item["result"]
    # 落库时 5 幅按 0.8 切成 4/1，列表读回不得重切成 2/3 或并侧
    assert res["left_ratio"] == 0.8
    assert (res["left_panels"], res["right_panels"]) == (4, 1)
    assert res["left_panels"] + res["right_panels"] == res["panels"] == 5
    assert "open_rebalanced" not in res
    # 总米数仍按总幅乘裁高，与分幅无关
    assert res["meters"] == round(res["panels"] * res["cut_height"], 2)


def test_default_ratio_change_does_not_rebalance_old_run(client):
    first = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "save": True, "left_ratio": 0.8,
    }).json()
    first_id = first["run_id"]
    # 之后再按默认 0.5 落一单，旧单详情仍须是写入时的 4/1
    client.post("/api/estimate", json={"window_id": 1, "fabric_id": 1, "save": True})
    old = client.get(f"/api/runs/{first_id}").json()["result"]
    assert old["left_ratio"] == 0.8
    assert (old["left_panels"], old["right_panels"]) == (4, 1)
