from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2

from core_pla_2049_engine.vector_processing.vector_field import VectorField
from core_pla_2049_engine.vector_processing.vector_cleaner import VectorCleaner
from core_pla_2049_engine.vector_processing.vector_aggregator import VectorAggregator
from core_pla_2049_engine.optical_flow_adapters.farneback_adapter import FarnebackOpticalFlow
from core_pla_2049_engine.coherent_regions.region_builder import RegionBuilder
from core_pla_2049_engine.coherent_regions.region_cluster import RegionCluster
from core_pla_2049_engine.region_graphs.graph_analyzer import RegionGraphAnalyzer


app = FastAPI(title="Near-Miss Detector", version="1.0")

flow_engine = FarnebackOpticalFlow()
cleaner = VectorCleaner()
aggregator = VectorAggregator()
region_builder = RegionBuilder()
clusterer = RegionCluster()
graph_analyzer = RegionGraphAnalyzer()


def load_image(file_bytes: bytes):
    img_array = np.frombuffer(file_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
    return img


def compute_near_miss_score(region_pairs):
    # Simplified scoring placeholder
    # Real scoring would consider angle changes, velocity vectors, collision courses, etc.
    return len(region_pairs) * 0.1


@app.post("/detect")
async def detect_near_miss(
    prev_frame: UploadFile = File(...),
    next_frame: UploadFile = File(...)
):
    prev_bytes = await prev_frame.read()
    next_bytes = await next_frame.read()

    prev_img = load_image(prev_bytes)
    next_img = load_image(next_bytes)

    # Step 1: Compute optical flow
    flow = flow_engine.compute(prev_img, next_img)
    flow = cleaner.smooth(flow)
    flow = cleaner.remove_outliers(flow)

    # Step 2: Vector processing
    aggregated = aggregator.aggregate(flow)
    regions = region_builder.build_regions(aggregated)
    clusters = clusterer.cluster(regions)

    # Step 3: Analyze adjacency / potential conflicts
    region_graph = graph_analyzer.dominant_flows({i: c['regions'] for i, c in enumerate(clusters)})

    # Step 4: Compute near-miss score (placeholder)
    score = compute_near_miss_score(region_graph)

    return {
        "region_count": len(regions),
        "cluster_count": len(clusters),
        "dominant_flows": region_graph,
        "near_miss_score": score
    }
