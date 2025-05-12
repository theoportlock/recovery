#!/bin/bash
set -e

SCRIPT="$1"
shift
ARGS="$@"

if [ -z "$SCRIPT" ]; then
  echo "Usage: $0 <script> [args...]"
  exit 1
fi

echo "Running $SCRIPT with args: $ARGS"
make run SCRIPT="$SCRIPT" ARGS="$ARGS"
