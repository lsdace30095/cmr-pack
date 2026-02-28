# Near-Miss Detector™ (NMD)
The Near-Miss Detector is a core real-time safety analytics microservice within the Sense Traffic Pulse™ platform.  
It uses patented Coherent Motion Region analytics (PLA-2049) to identify potential conflicts between vehicles, cyclists, and pedestrians.

## 🚦 Features
- Accepts raw grayscale frame pairs as input
- Computes optical flow to detect motion vectors
- Forms coherent motion regions (PLA-2049 protected process)
- Clusters regions into flow groups
- Detects potential conflicts based on region distribution
- Outputs a near-miss risk score
- FastAPI microservice (A1 architecture)
- Azure-ready (Container Apps, AKS)

## 📁 Project Structure
```
near-miss-detector/
│
├── main.py                    # FastAPI entrypoint
├── services/
│   └── near_miss_service.py   # Near-miss analysis logic
├── models/
│   ├── response_schema.py     # Pydantic response schemas
│   └── frame_input.py         # Frame metadata schema
├── deploy/
│   └── azure/
│       ├── containerapp.yaml  # Azure Container App definition
│       ├── ingress.yaml       # AKS ingress manifest
│       └── env.example        # Environment variable template
├── tests/
│   └── __init__.py
└── Dockerfile
```

## 🧠 How It Works (Pipeline)
1. Upload two sequential frames to `/detect`
2. Compute optical flow between frames
3. Smooth and clean the vector field
4. Aggregate vectors into local motion units
5. Build coherent motion regions (patented method)
6. Cluster regions into flow groups
7. Detect potential conflict zones
8. Compute a near-miss risk score

## 📘 API Usage
### `POST /detect`
**Inputs:**  
- `prev_frame`: JPEG/PNG  
- `next_frame`: JPEG/PNG  

**Returns:**
```
{
  "region_count": <int>,
  "cluster_count": <int>,
  "conflict_indices": [...],
  "near_miss_score": <float>
}
```

## 🏗 Deployment Instructions
### Local Docker
```
docker build -t nmd .
docker run -p 8000:8000 nmd
```

### Azure Container Apps
```
az containerapp up   --name near-miss-detector   --resource-group <RG>   --environment <ENV_ID>   --image <ACR_SERVER>/near-miss-detector:latest
```

## 🛡 Intellectual Property
The near-miss analysis pipeline relies on region formation and vector aggregation methods protected under PLA-2049.  
Dace IT LLC holds exclusive commercial rights. Unauthorized replication may constitute infringement.

## 📞 Contact
Sense Traffic Pulse™ by Dace IT LLC  
For OEM licensing or Smart City integration: partners@sensetrafficpulse.com
