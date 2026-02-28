import numpy as np
import cv2

from core_pla_2049_engine.optical_flow_adapters.farneback_adapter import FarnebackOpticalFlow
from core_pla_2049_engine.vector_processing.vector_cleaner import VectorCleaner
from core_pla_2049_engine.vector_processing.vector_aggregator import VectorAggregator
from core_pla_2049_engine.coherent_regions.region_builder import RegionBuilder
from core_pla_2049_engine.coherent_regions.region_cluster import RegionCluster


class AnomalyService:
    """Service module for detecting anomalous traffic behavior using PLA-2049 coherent motion regions."""

    def __init__(self):
        self.flow_engine = FarnebackOpticalFlow()
        self.cleaner = VectorCleaner()
        self.aggregator = VectorAggregator()
        self.region_builder = RegionBuilder()
        self.clusterer = RegionCluster()

    def compute_flow(self, prev_img, next_img):
        """Compute optical flow and smooth it."""
        flow = self.flow_engine.compute(prev_img, next_img)
        flow = self.cleaner.smooth(flow)
        return flow

    def build_regions(self, flow):
        """Aggregate vectors and generate motion regions."""
        aggregated = self.aggregator.aggregate(flow)
        return self.region_builder.build_regions(aggregated)

    def cluster_regions(self, regions):
        """Cluster coherent regions into macro flows."""
        return self.clusterer.cluster(regions)

    def detect_anomalies(self, regions, clusters):
        """Detect anomalies via simple heuristics (expandable)."""
        anomalies = []

        # Too little movement (possible stalled traffic)
        if len(regions) < 3:
            anomalies.append("Low motion anomaly")

        # Excessive motion (crowd surges, panic, abnormal events)
        if len(regions) > 30:
            anomalies.append("High-density motion anomaly")

        # Excessive fragmentation (chaotic flow behavior)
        if len(clusters) > 10:
            anomalies.append("Flow fragmentation anomaly")

        return anomalies

    def analyze(self, prev_img, next_img):
        """Complete anomaly detection pipeline."""
        flow = self.compute_flow(prev_img, next_img)
        regions = self.build_regions(flow)
        clusters = self.cluster_regions(regions)
        anomalies = self.detect_anomalies(regions, clusters)

        return {
            "region_count": len(regions),
            "cluster_count": len(clusters),
            "anomalies": anomalies
        }
