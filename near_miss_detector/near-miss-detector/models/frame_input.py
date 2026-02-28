from pydantic import BaseModel

class NearMissFrameInput(BaseModel):
    description: str = "Two sequential grayscale frames uploaded for near-miss detection."
