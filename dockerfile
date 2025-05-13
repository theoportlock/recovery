FROM python:3.10-slim

LABEL description="Pipeline Docker Image"
LABEL maintainer="theo@portlocklab.com"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    git \
    fonts-dejavu-core \
    fonts-liberation \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY matplotlibrc .
