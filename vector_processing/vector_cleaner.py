import numpy as np
import cv2

class VectorCleaner:
    """Cleans noisy vector fields using smoothing and masking strategies."""

    def smooth(self, flow):
        return cv2.GaussianBlur(flow, (5,5), 0)

    def remove_outliers(self, flow, threshold=5.0):
        mag = np.sqrt(flow[...,0]**2 + flow[...,1]**2)
        mask = mag < threshold
        return flow * mask[..., None]
