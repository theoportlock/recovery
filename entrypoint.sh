#!/usr/bin/env bash
set -e

echo "[entrypoint] PWD=$(pwd)"
echo "[entrypoint] DATA=${DATA}"
echo "[entrypoint] PATH=${PATH}"

exec "$@"

