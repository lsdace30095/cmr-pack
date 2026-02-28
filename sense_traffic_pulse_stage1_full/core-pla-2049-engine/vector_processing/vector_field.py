import numpy as np

class VectorField:
    """Represents a 2D motion vector field derived from optical flow."""

    def __init__(self, flow):
        self.flow = flow

    def magnitude(self):
        return np.sqrt(self.flow[..., 0] ** 2 + self.flow[..., 1] ** 2)

    def direction(self):
        return np.arctan2(self.flow[..., 1], self.flow[..., 0])
