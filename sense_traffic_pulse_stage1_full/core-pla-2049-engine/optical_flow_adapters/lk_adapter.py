import cv2
import numpy as np

class LucasKanadeOpticalFlow:
    def __init__(self):
        self.lk_params = dict(
            winSize=(15, 15),
            maxLevel=2,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
        )

    def compute(self, prev_frame, next_frame):
        p0 = cv2.goodFeaturesToTrack(prev_frame, mask=None, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
        p1, st, err = cv2.calcOpticalFlowPyrLK(prev_frame, next_frame, p0, None, **self.lk_params)
        return p0, p1, st
