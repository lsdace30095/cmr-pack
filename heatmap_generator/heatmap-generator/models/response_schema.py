from pydantic import BaseModel

class HeatmapResponse(BaseModel):
    height: int
    width: int
    heatmap_image_base64: str
