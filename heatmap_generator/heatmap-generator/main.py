from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2

from core_pla_2049_engine.vector_processing.vector_cleaner import VectorCleaner
from core_pla_2049_engine.vector_processing.vector_aggregator import VectorAggregator
from core_pla_2049_engine.optical_flow_adapters.farneback_adapter import FarnebackOpticalFlow
from core_pla_2049_engine.coherent_regions.region_builder import RegionBuilder
from core_pla_2049_engine.coherent_regions.region_cluster import RegionCluster


app = FastAPI(title="Heatmap Generator", version="1.0")

flow_engine = FarnebackOpticalFlow()
cleaner = VectorCleaner()
aggregator = VectorAggregator()
region_builder = RegionBuilder()
clusterer = RegionCluster()


def load_image(file_bytes: bytes):
    img_array = np.frombuffer(file_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
    return img


def generate_heatmap(flow, height, width):
    mag = np.sqrt(flow[..., 0] ** 2 + flow[..., 1] ** 2)
    heatmap = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    heatmap = heatmap.astype(np.uint8)
    colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    _, encoded = cv2.imencode(".jpg", colored)
    return encoded.tobytes()


@app.post("/heatmap")
async def heatmap(
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

    # Step 2: Heatmap generation
    h, w = prev_img.shape
    heatmap_bytes = generate_heatmap(flow, h, w)

    return {
        "height": h,
        "width": w,
        "heatmap_image_base64": heatmap_bytes.hex()
    }
