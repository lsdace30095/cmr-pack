import os

class Config:
    """Loads runtime configuration for the PLA-2049 engine."""

    @staticmethod
    def get_flow_model_path():
        path = os.getenv("FLOW_MODEL_PATH")
        if not path:
            raise ValueError("FLOW_MODEL_PATH is not set")
        return path
