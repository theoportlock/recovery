#!/usr/bin/env bash
set -euo pipefail

IMAGE="theoportlock/m4efad-image:latest"
WORKDIR="/workspace"

# Check or build image
if ! docker image inspect "$IMAGE" &>/dev/null; then
    echo "Docker image not found. Building..."
    docker build -t "$IMAGE" .
fi

# Custom paths for scripts
CUSTOM_PATH="/workspace/code:/workspace/metatoolkit/metatoolkit:/workspace/metaphlan/metaphlan/utils:$PATH"

# Run the container
docker run --rm -it \
    -v "$(pwd)":$WORKDIR \
    -w $WORKDIR \
    -e PATH="$CUSTOM_PATH" \
    "$IMAGE" "$@"

