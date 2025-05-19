FROM python:3.10-slim

LABEL description="Pipeline Docker Image"
LABEL maintainer="theo@portlocklab.com"

WORKDIR /app

# Install system dependencies including R and GNU Parallel
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    git \
    fonts-dejavu-core \
    fonts-liberation \
    curl \
    r-base \
    r-base-dev \
    gfortran \
    libxml2-dev \
    libssl-dev \
    libcurl4-openssl-dev \
    parallel \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install MaAsLin2 in R
RUN Rscript -e "install.packages('BiocManager', repos='https://cloud.r-project.org')" && \
    Rscript -e "BiocManager::install('Maaslin2')"

# Optional: add Maaslin2.R to PATH
ENV PATH="/usr/local/lib/R/site-library/Maaslin2:${PATH}"

# Copy local files
COPY matplotlibrc .

# (Optional) You may want to add a default CMD or ENTRYPOINT if this will be used directly
