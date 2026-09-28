import json
from datetime import datetime, timezone
from app.db import connect

_RUN_SELECT = """SELECT r.*, w.name window_name, f.name fabric_name FROM calc_runs r
LEFT JOIN windows w ON w.id=r.window_id LEFT JOIN fabrics f ON f.id=r.fabric_id"""

def _row_to_dict(row):
    d = dict(row)
    # 原样返回落库时的分幅结果：不得在打开详情/列表时按现行默认占比重切旧单。
    d["result"] = json.loads(d.pop("result_json"))
    return d

def insert_run(window_id, fabric_id, result, note=""):
    c = connect()
    try:
        cur = c.execute(
            "INSERT INTO calc_runs(window_id,fabric_id,result_json,note,created_at) VALUES (?,?,?,?,?)",
            (window_id, fabric_id, json.dumps(result, ensure_ascii=False), note, datetime.now(timezone.utc).isoformat()),
        )
        c.commit()
        return int(cur.lastrowid)
    finally:
        c.close()

def get_run(run_id):
    c = connect()
    try:
        row = c.execute(_RUN_SELECT + " WHERE r.id=?", (run_id,)).fetchone()
        return _row_to_dict(row) if row else None
    finally:
        c.close()

def list_runs(limit=50, window_id=None):
    c = connect()
    try:
        if window_id is not None:
            rows = c.execute(
                _RUN_SELECT + " WHERE r.window_id=? ORDER BY r.id DESC LIMIT ?",
                (window_id, limit),
            ).fetchall()
        else:
            rows = c.execute(
                _RUN_SELECT + " ORDER BY r.id DESC LIMIT ?", (limit,)).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        c.close()
