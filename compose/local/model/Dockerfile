# Use an NVIDIA CUDA base image with development tools
FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and Python
RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    ffmpeg \
    libsm6 \
    libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add CUDA paths
ENV PATH=/usr/local/cuda/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Copy the requirements file
COPY ./requirements /requirements

# Install Python packages including PyTorch with CUDA support
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements/model.txt

# Copy and set up the start script
COPY ./compose/local/model/start /start
RUN sed -i 's/\r//' /start && \
    chmod +x /start

WORKDIR /app
