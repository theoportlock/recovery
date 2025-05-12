FROM python:3.11-slim

LABEL description="Pipeline Docker Image"
LABEL maintainer="theo@portlocklab.com"

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Clone and set up metatoolkit
RUN git clone https://github.com/theoportlock/metatoolkit.git /app/metatoolkit
    cd /app/metatoolkit
    pip install .

# Copy in your code and configurations
COPY code/ ./code/
COPY conf/ ./conf/
COPY matplotlibrc .
COPY README.md .

# Optional: set up a useful PYTHONPATH
ENV PYTHONPATH="/app/code:${PYTHONPATH}"
