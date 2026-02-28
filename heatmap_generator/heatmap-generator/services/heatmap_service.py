import numpy as np
import cv2

from core_pla_2049_engine.optical_flow_adapters.farneback_adapter import FarnebackOpticalFlow
from core_pla_2049_engine.vector_processing.vector_cleaner import VectorCleaner
from core_pla_2049_engine.vector_processing.vector_aggregator import VectorAggregator


class HeatmapService:
    """Service module for generating motion-intensity heatmaps from sequential video frames."""

    def __init__(self):
        self.flow_engine = FarnebackOpticalFlow()
        self.cleaner = VectorCleaner()
        self.aggregator = VectorAggregator()

    def compute_flow(self, prev_img, next_img):
        """Compute and clean optical flow between two grayscale frames."""
        flow = self.flow_engine.compute(prev_img, next_img)
        flow = self.cleaner.smooth(flow)
        return flow

    def generate_heatmap(self, flow):
        """Generate a colorized heatmap from optical flow magnitude."""
        mag = np.sqrt(flow[..., 0] ** 2 + flow[..., 1] ** 2)
        heatmap = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        heatmap = heatmap.astype(np.uint8)
        colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        return colored

    def encode_heatmap(self, heatmap_img):
        """Encode heatmap as JPEG for API response."""
        _, encoded = cv2.imencode(".jpg", heatmap_img)
        return encoded.tobytes()

    def analyze(self, prev_img, next_img):
        """Full pipeline for heatmap analysis."""
        flow = self.compute_flow(prev_img, next_img)
        heatmap = self.generate_heatmap(flow)
        encoded = self.encode_heatmap(heatmap)

        h, w = heatmap.shape[:2]

        return {
            "height": h,
            "width": w,
            "heatmap_image_base64": encoded.hex()
        }
