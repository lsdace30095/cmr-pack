from fastapi import FastAPI, UploadFile, File
from core_pla_2049_engine.optical_flow_adapters.farneback_adapter import FarnebackOpticalFlow
from core_pla_2049_engine.vector_processing.vector_field import VectorField
from core_pla_2049_engine.vector_processing.vector_cleaner import VectorCleaner
from core_pla_2049_engine.vector_processing.vector_aggregator import VectorAggregator
from core_pla_2049_engine.coherent_regions.region_builder import RegionBuilder
from core_pla_2049_engine.coherent_regions.region_cluster import RegionCluster
from core_pla_2049_engine.region_graphs.graph_analyzer import RegionGraphAnalyzer
import cv2
import numpy as np
import io
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Intersection Flow Engine", version="1.0")

# Initialize engines
try:
    flow_engine = FarnebackOpticalFlow()
    cleaner = VectorCleaner()
    aggregator = VectorAggregator()
    region_builder = RegionBuilder()
    clusterer = RegionCluster()
    graph_analyzer = RegionGraphAnalyzer()
    logger.info("All modules imported successfully")
except Exception as e:
    logger.error(f"Failed to import modules: {e}")
    logger.error(traceback.format_exc())
    raise

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Intersection Flow Engine"}

def load_image(file_bytes: bytes):
    img_array = np.frombuffer(file_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
    return img

@app.post("/analyze")
async def analyze(
    prev_frame: UploadFile = File(...),
    next_frame: UploadFile = File(...)
):
    try:
        prev_bytes = await prev_frame.read()
        next_bytes = await next_frame.read()

        prev_img = load_image(prev_bytes)
        next_img = load_image(next_bytes)

        # Step 1: Optical flow
        flow = flow_engine.compute(prev_img, next_img)

        # Step 2: Clean flow
        flow = cleaner.smooth(flow)
        flow = cleaner.remove_outliers(flow)

        # Step 3: Vector aggregation
        aggregated = aggregator.aggregate(flow)

        # Step 4: Build coherent regions
        regions = region_builder.build_regions(aggregated)

        # Step 5: Cluster regions
        clusters = clusterer.cluster(regions)

        # Step 6: Analyze region graph
        graph = graph_analyzer.dominant_flows({i: c['regions'] for i, c in enumerate(clusters)})

        # Step 7: Build response
        response = {
            "flows": {
                "dominant_flows": graph
            },
            "region_count": len(regions),
            "cluster_count": len(clusters)
        }

        return response
    except Exception as e:
        logger.error(f"Error in analyze: {e}")
        logger.error(traceback.format_exc())
        return {"error": str(e)}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
