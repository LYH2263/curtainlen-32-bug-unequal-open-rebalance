from fastapi import APIRouter, HTTPException
from app.repositories import history as repo
router = APIRouter()
@router.get("/runs")
def runs(limit: int = 50, window_id: int | None = None):
    return {"items": repo.list_runs(limit, window_id)}
@router.get("/runs/{run_id}")
def get_run(run_id: int):
    r = repo.get_run(run_id)
    if not r:
        raise HTTPException(404, "run not found")
    return r
