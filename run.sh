#!/usr/bin/env bash
set -e

IMAGE="theoportlock/m4efad-image:latest"
WORKDIR="/workspace"

# Build image if missing
if ! docker image inspect "$IMAGE" &>/dev/null; then
    echo "Docker image not found. Building..."
    docker build -t "$IMAGE" .
fi

# Ensure at least a script name is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <script> [args...]"
    exit 1
fi

SCRIPT=$1
shift

# Search for the script
if [[ -f "code/$SCRIPT" ]]; then
    SCRIPT_PATH="code/$SCRIPT"
elif [[ -f "metatoolkit/metatoolkit/$SCRIPT" ]]; then
    SCRIPT_PATH="metatoolkit/metatoolkit/$SCRIPT"
elif [[ -f "$SCRIPT" ]]; then
    SCRIPT_PATH="$SCRIPT"
else
    echo "Error: script '$SCRIPT' not found in code/, metatoolkit/metatoolkit/, or current directory."
    exit 1
fi

# Run inside Docker with appropriate mounts and PATH
docker run --rm -it \
  -v "$(pwd)":$WORKDIR \
  -w $WORKDIR \
  -e PATH="$WORKDIR/code:$WORKDIR/metatoolkit/metatoolkit:\$PATH" \
  "$IMAGE" \
  "./$SCRIPT_PATH" "$@"
