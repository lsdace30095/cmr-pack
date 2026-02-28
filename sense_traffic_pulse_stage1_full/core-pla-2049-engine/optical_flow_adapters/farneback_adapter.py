import cv2
import numpy as np

class FarnebackOpticalFlow:
    def __init__(self):
        self.params = dict(
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0
        )

    def compute(self, prev_frame, next_frame):
        flow = cv2.calcOpticalFlowFarneback(
            prev_frame, next_frame, None, **self.params
        )
        return flow
