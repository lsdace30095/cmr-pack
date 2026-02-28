from pydantic import BaseModel
from typing import List, Any

class NearMissConflict(BaseModel):
    conflict_region_index: int
    description: str = "Potential conflict detected in this flow cluster."

class NearMissResponse(BaseModel):
    region_count: int
    cluster_count: int
    conflict_indices: List[int]
    near_miss_score: float
