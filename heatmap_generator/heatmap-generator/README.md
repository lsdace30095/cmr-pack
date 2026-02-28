# Heatmap Generator™ (HG)
The Heatmap Generator is a core microservice within the Sense Traffic Pulse™ platform.  
It converts motion vectors into high-resolution motion-intensity heatmaps using the patented PLA-2049 Coherent Motion Region framework.

## 🔥 Purpose
- Visualize motion intensity across an intersection
- Reveal congestion hotspots
- Support traffic flow optimization
- Enable Smart City dashboards and digital twins
- Provide OEMs with spatial analytics for camera systems

## 🚦 Features
- Accepts two sequential grayscale frames (F1 input mode)
- Computes dense optical flow using Farneback (RAFT-lite optional)
- Cleans and normalizes motion vectors
- Generates colorized Jet heatmaps
- Encodes heatmaps as JPEG (base64 hex for API responses)
- Azure-ready deployment
- Fully containerized (Docker)

## 📁 Project Structure
```
heatmap-generator/
│
├── main.py                     # FastAPI entrypoint
├── services/
│   └── heatmap_service.py      # Heatmap analysis logic
├── models/
│   ├── response_schema.py      # Output schema
│   └── frame_input.py          # Input metadata schema
├── deploy/
│   └── azure/
│       ├── containerapp.yaml   # Azure Container App definition
│       ├── ingress.yaml        # AKS ingress definition
│       └── env.example         # Environment variable template
├── tests/
│   └── __init__.py
└── Dockerfile
```

## 🧠 How It Works (Pipeline)
1. User uploads two sequential grayscale frames to `/heatmap`
2. Optical flow is computed between the frames
3. Vector magnitudes are normalized
4. Heatmap is colorized using `COLORMAP_JET`
5. JPEG is encoded and returned as base64 hex

## 📘 API Usage
### `POST /heatmap`
**Inputs:**  
- `prev_frame`: JPEG/PNG  
- `next_frame`: JPEG/PNG  

**Returns (JSON):**
```
{
  "height": <int>,
  "width": <int>,
  "heatmap_image_base64": "<hex>"
}
```

## 🏗 Deployment Instructions
### Local Docker
```
docker build -t heatmap-generator .
docker run -p 8000:8000 heatmap-generator
```

### Azure Container Apps
```
az containerapp up   --name heatmap-generator   --resource-group <RG>   --environment <ENV_ID>   --image <ACR_SERVER>/heatmap-generator:latest
```

## 🛡 Intellectual Property
This microservice uses motion aggregation and region formation methods protected under PLA-2049.  
Dace IT LLC holds exclusive commercial rights in the United States.

## 📞 Contact
Sense Traffic Pulse™ by Dace IT LLC  
Partner Integrations: partners@sensetrafficpulse.com
