from pydantic import BaseModel
from typing import List

class AnomalyDetail(BaseModel):
    code: str
    description: str

class AnomalyResponse(BaseModel):
    region_count: int
    cluster_count: int
    anomalies: List[str]
