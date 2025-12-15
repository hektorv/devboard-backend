#!/usr/bin/env bash
set -euo pipefail

echo "Running tests..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest -q --maxfail=1 --cov=app
