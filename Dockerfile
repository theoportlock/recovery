FROM python:3.10-slim

LABEL description="Development toolbox (Python + R + MaAsLin3)"
LABEL maintainer="theo@portlocklab.com"

# ---- Base environment ----
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# ---- System dependencies ----
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
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ---- R packages ----
RUN Rscript -e "install.packages(c('remotes', 'devtools', 'BiocManager'), repos='https://cloud.r-project.org')" && \
    Rscript -e "remotes::install_github('biobakery/maaslin3')" && \
    Rscript -e "BiocManager::install(c( \
        'microbiome', 'rhdf5filters', 'sp', 'rhdf5', 'UCSC.utils', \
        'GenomeInfoDbData', 'ade4', 'biomformat', 'igraph', \
        'multtest', 'S4Vectors', 'IRanges', 'XVector', 'GenomeInfoDb', \
        'phyloseq', 'Biostrings', 'Rtsne' \
    ), ask = FALSE, update = TRUE)"

# ---- Python dependencies ----
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# ---- Matplotlib defaults ----
COPY matplotlibrc /etc/matplotlibrc

# ---- Runtime environment ----
ENV WORKDIR=/work
ENV DATA=/data

ENV PATH="/work/code:\
/work/metatoolkit/metatoolkit:\
/work/maaslin3/R:\
/work/digital_twin/scripts:${PATH}"

# ---- Entrypoint ----
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ---- Non-root user ----
RUN useradd -m -u 1000 appuser
USER appuser

WORKDIR /work

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]

