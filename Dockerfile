FROM python:3.10-slim

LABEL description="Pipeline Docker Image for m4efad"
LABEL maintainer="theo@portlocklab.com"

WORKDIR /app

# Install system dependencies including R and GNU Parallel
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libxml2-dev \
    libssl-dev \
    libcurl4-openssl-dev \
    libgit2-dev \
    fonts-dejavu-core \
    fonts-liberation \
    git \
    curl \
    r-base \
    r-base-dev \
    gfortran \
    parallel \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install R packages including MaAsLin2
RUN Rscript -e "install.packages(c('remotes', 'devtools'), repos='https://cloud.r-project.org')" && \
    Rscript -e "remotes::install_github('biobakery/maaslin3')"

# Skip setting Bioconductor version manually
RUN Rscript -e "install.packages('BiocManager', repos='https://cloud.r-project.org')" && \
    Rscript -e "BiocManager::install(c( \
        'microbiome', 'rhdf5filters', 'sp', 'rhdf5', 'UCSC.utils', \
        'GenomeInfoDbData', 'ade4', 'biomformat', 'igraph', \
        'multtest', 'S4Vectors', 'IRanges', 'XVector', 'GenomeInfoDb', \
        'phyloseq', 'Biostrings', 'Rtsne' \
    ), ask = FALSE, update = TRUE)"

# Install Python packages
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Add matplotlibrc config
COPY matplotlibrc .

# Default shell
CMD ["/bin/bash"]

