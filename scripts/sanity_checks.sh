#!/usr/bin/env bash
set -euo pipefail

nvidia-smi || { echo "nvidia-smi failed"; exit 1; }

source .venv/bin/activate
python src/check_cuda.py
