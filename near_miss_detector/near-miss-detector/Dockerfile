# Near-Miss Detector Dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all service files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn numpy opencv-python-headless onnxruntime

# Expose API port
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
