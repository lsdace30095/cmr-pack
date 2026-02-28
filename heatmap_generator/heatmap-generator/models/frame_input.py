from pydantic import BaseModel

class HeatmapFrameInput(BaseModel):
    description: str = "Two sequential grayscale frames uploaded to produce a motion-intensity heatmap."
