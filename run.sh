#!/bin/bash
set -e

if [ $# -lt 1 ]; then
  echo "Usage: $0 <script> [args...]"
  exit 1
fi

echo "Running command: $@"
make run COMMAND="$*"
