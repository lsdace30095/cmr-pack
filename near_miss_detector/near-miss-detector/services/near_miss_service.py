import numpy as np
import cv2

from core_pla_2049_engine.optical_flow_adapters.farneback_adapter import FarnebackOpticalFlow
from core_pla_2049_engine.vector_processing.vector_cleaner import VectorCleaner
from core_pla_2049_engine.vector_processing.vector_aggregator import VectorAggregator
from core_pla_2049_engine.coherent_regions.region_builder import RegionBuilder
from core_pla_2049_engine.coherent_regions.region_cluster import RegionCluster
from core_pla_2049_engine.region_graphs.graph_analyzer import RegionGraphAnalyzer


class NearMissService:
    """Service module for detecting near-miss events using coherent motion regions."""

    def __init__(self):
        self.flow_engine = FarnebackOpticalFlow()
        self.cleaner = VectorCleaner()
        self.aggregator = VectorAggregator()
        self.region_builder = RegionBuilder()
        self.clusterer = RegionCluster()
        self.graph_analyzer = RegionGraphAnalyzer()

    def compute_flow(self, prev_img, next_img):
        """Extract and clean optical flow from frames."""
        flow = self.flow_engine.compute(prev_img, next_img)
        flow = self.cleaner.smooth(flow)
        flow = self.cleaner.remove_outliers(flow)
        return flow

    def build_regions(self, flow):
        """Aggregate vectors and form coherent motion regions."""
        aggregated = self.aggregator.aggregate(flow)
        regions = self.region_builder.build_regions(aggregated)
        return regions

    def cluster_regions(self, regions):
        """Cluster coherent regions into macro flow groups."""
        return self.clusterer.cluster(regions)

    def detect_conflicts(self, clusters):
        """Detect potential near-miss conflicts between region clusters."""
        # Placeholder heuristic:
        conflicts = []
        for idx, cluster in enumerate(clusters):
            if len(cluster['regions']) > 2:
                conflicts.append(idx)
        return conflicts

    def compute_near_miss_score(self, conflicts):
        """Compute a risk score based on detected conflicts."""
        return len(conflicts) * 0.15

    def analyze(self, prev_img, next_img):
        """Full near-miss analysis pipeline."""

        flow = self.compute_flow(prev_img, next_img)
        regions = self.build_regions(flow)
        clusters = self.cluster_regions(regions)
        conflicts = self.detect_conflicts(clusters)
        score = self.compute_near_miss_score(conflicts)

        return {
            "region_count": len(regions),
            "cluster_count": len(clusters),
            "conflict_indices": conflicts,
            "near_miss_score": score
        }
