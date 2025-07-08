#!/usr/bin/env bash
set -e

IMAGE="theoportlock/m4efad-image:latest"
WORKDIR="/workspace"

# Build image if missing
if ! docker image inspect "$IMAGE" &>/dev/null; then
    echo "Docker image not found. Building..."
    docker build -t "$IMAGE" .
fi

# Run inside Docker with mounts and default PATH
docker run --rm -it \
  -v "$(pwd)":$WORKDIR \
  -w $WORKDIR \
  -e PATH="$WORKDIR/Maaslin2/R:$WORKDIR/code:$WORKDIR/metatoolkit/metatoolkit:$PATH" \
  "$IMAGE" \
  "$@"

