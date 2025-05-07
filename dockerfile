FROM python:3.11-slim

LABEL description="Pipeline Docker Image"
LABEL maintainer="theo@portlocklab.com"
WORKDIR /app

# System dependencies (add more if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install your Python package and dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .
