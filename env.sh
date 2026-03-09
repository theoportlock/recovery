#!/usr/bin/env bash
# Environment setup for fellowship project

# Data path
export data="/mnt/d/fellowship/m4efad/recovery/data"

# Add project paths to PATH
export PATH="code/:$PATH"
export PATH="metatoolkit/metatoolkit/:$PATH"
export PATH="maaslin3/R/:$PATH"
export PATH="digital_twin/scripts/:$PATH"

# Activate environment
#source ~/miniconda3/etc/profile.d/conda.sh
#conda activate metatoolkit

#bash -lc "\
#  source ~/miniconda3/etc/profile.d/conda.sh &&\
#  conda activate metatoolkit && \
#  {} \
#  "

source venv/bin/activate
