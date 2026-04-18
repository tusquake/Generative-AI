# Use a lightweight PyTorch base image with CUDA support
# This handles the complex CUDA + Python + PyTorch link for us
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies for image processing (Pillow/OpenCV)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
