from pydantic import BaseModel, Field

class EstimateRequest(BaseModel):
    window_id: int
    fabric_id: int
    save: bool = False
    note: str = ""
    left_ratio: float = Field(default=0.5, ge=0.0, le=1.0)
