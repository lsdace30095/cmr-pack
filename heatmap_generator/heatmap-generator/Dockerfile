# Heatmap Generator Dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy microservice files
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir fastapi uvicorn numpy opencv-python-headless onnxruntime

# Expose API port
EXPOSE 8000

# Start the FastAPI service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
