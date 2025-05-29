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

# Install Python packages
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install MaAsLin2 in R (from GitHub)
RUN Rscript -e "install.packages(c('remotes', 'devtools'), repos='https://cloud.r-project.org')" && \
    Rscript -e "remotes::install_github('biobakery/Maaslin2')"

# Optional: copy in Maaslin2.R wrapper script and make executable
COPY code/Maaslin2.R /usr/local/bin/
RUN chmod +x /usr/local/bin/Maaslin2.R

# Optional: matplotlib config
COPY matplotlibrc .

# Add any ENV changes (if needed)
ENV PATH="/usr/local/bin:${PATH}"

# Default command (optional)
CMD ["/bin/bash"]
