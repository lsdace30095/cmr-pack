# Anomaly Detector Dockerfile
FROM python:3.10-slim

# Install OpenCV and system-level deps
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy microservice contents
COPY . /app

# Install runtime dependencies
RUN pip install --no-cache-dir fastapi uvicorn numpy opencv-python-headless onnxruntime

# Expose FastAPI port
EXPOSE 8000

# Run API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
