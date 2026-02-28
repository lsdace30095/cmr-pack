from pydantic import BaseModel

class AnomalyFrameInput(BaseModel):
    description: str = "Two sequential grayscale frames uploaded for anomaly detection."
