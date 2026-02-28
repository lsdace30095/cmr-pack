# Anomaly Detector™ (AD)
The Anomaly Detector is a real-time microservice in the Sense Traffic Pulse™ platform designed to identify unusual traffic behaviors using PLA-2049 patented motion-region analytics.

## 🎯 Purpose
Detect abnormal traffic behaviors such as:
- Wrong-way movement
- Sudden surges or density spikes
- Abnormally low motion (dead zones, stalled vehicles)
- Excessive flow fragmentation (chaotic or conflicting flows)
- Irregular region pattern shifts

## 🚀 Features
- Accepts two sequential grayscale frames (F1 input mode)
- Computes dense optical flow
- Builds coherent motion regions (PLA-2049 protected process)
- Clusters regions into flow groups
- Identifies anomalies based on region & flow metrics
- JSON-based anomaly reports
- Deployable on Azure Container Apps or AKS

## 📁 Project Structure
```
anomaly-detector/
│
├── main.py                      # FastAPI anomaly detection API
├── services/
│   └── anomaly_service.py       # Full anomaly detection logic
├── models/
│   ├── response_schema.py       # Typed output schema
│   └── frame_input.py           # Input metadata schema
├── deploy/
│   └── azure/
│       ├── containerapp.yaml    # Azure Container Apps config
│       ├── ingress.yaml         # AKS ingress config
│       └── env.example          # Environment template
├── tests/
│   └── __init__.py
└── Dockerfile                   # Production-ready container build
```

## 🔧 How It Works (Pipeline)
1. User submits 2 sequential frames to `/detect-anomaly`
2. Optical flow is computed
3. Vector field is smoothed and cleaned
4. Coherent motion regions are generated (PLA-2049)
5. Regions are clustered into flows
6. Heuristics detect abnormalities
7. Service returns JSON anomaly summary

## 📘 API Usage
### `POST /detect-anomaly`
**Inputs:**  
- `prev_frame`: JPEG/PNG  
- `next_frame`: JPEG/PNG  

**Returns (JSON):**
```
{
  "region_count": <int>,
  "cluster_count": <int>,
  "anomalies": [
    "Low motion anomaly",
    "Flow fragmentation anomaly"
  ]
}
```

## 🏗 Deployment Instructions
### Local Docker
```
docker build -t anomaly-detector .
docker run -p 8000:8000 anomaly-detector
```

### Azure Container Apps
```
az containerapp up   --name anomaly-detector   --resource-group <RG>   --environment <ENV_ID>   --image <ACR_SERVER>/anomaly-detector:latest
```

## 🛡 Intellectual Property
This service uses region formation and flow analysis methods protected under PLA-2049, exclusively licensed to Dace IT LLC.  
Unauthorized replication may constitute patent infringement.

## 📞 Contact
Sense Traffic Pulse™ by Dace IT LLC  
OEM & Smart City Partnerships: partners@sensetrafficpulse.com
