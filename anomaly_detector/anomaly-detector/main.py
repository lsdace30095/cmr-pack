from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2

from core_pla_2049_engine.optical_flow_adapters.farneback_adapter import FarnebackOpticalFlow
from core_pla_2049_engine.vector_processing.vector_cleaner import VectorCleaner
from core_pla_2049_engine.vector_processing.vector_aggregator import VectorAggregator
from core_pla_2049_engine.coherent_regions.region_builder import RegionBuilder
from core_pla_2049_engine.coherent_regions.region_cluster import RegionCluster


app = FastAPI(title="Anomaly Detector", version="1.0")

flow_engine = FarnebackOpticalFlow()
cleaner = VectorCleaner()
aggregator = VectorAggregator()
region_builder = RegionBuilder()
clusterer = RegionCluster()


def load_image(file_bytes: bytes):
    img_array = np.frombuffer(file_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
    return img


def detect_anomalies(regions, clusters):
    """
    Simplified anomaly heuristic:
    - Too few regions
    - Too many regions
    - Sudden directional changes
    """
    anomalies = []

    if len(regions) < 3:
        anomalies.append("Abnormally low motion detected")

    if len(regions) > 30:
        anomalies.append("High-density movement anomaly")

    if len(clusters) > 10:
        anomalies.append("Excessive flow fragmentation")

    return anomalies


@app.post("/detect-anomaly")
async def detect_anomaly(
    prev_frame: UploadFile = File(...),
    next_frame: UploadFile = File(...)
):
    prev_bytes = await prev_frame.read()
    next_bytes = await next_frame.read()

    prev_img = load_image(prev_bytes)
    next_img = load_image(next_bytes)

    # Step 1: Optical flow
    flow = flow_engine.compute(prev_img, next_img)
    flow = cleaner.smooth(flow)

    # Step 2: Vector aggregation
    aggregated = aggregator.aggregate(flow)

    # Step 3: Build coherent regions & clusters
    regions = region_builder.build_regions(aggregated)
    clusters = clusterer.cluster(regions)

    # Step 4: Detect anomalies
    anomaly_list = detect_anomalies(regions, clusters)

    return {
        "region_count": len(regions),
        "cluster_count": len(clusters),
        "anomalies": anomaly_list
    }
