#!/usr/bin/env bash
# Start script to ensure $PORT is expanded by the shell
set -euo pipefail

: "Using PORT=${PORT:-8080}"
exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-8080}"
