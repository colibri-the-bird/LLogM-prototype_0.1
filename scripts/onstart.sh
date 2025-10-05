#!/usr/bin/env bash
set -euxo pipefail

# Load repo and user env if present
if [[ -f ./.env ]]; then source ./.env; fi
if [[ -f ./configs/runpod.env ]]; then source ./configs/runpod.env; fi

VOL=${RUNPOD_MOUNT_PATH:-/workspace}
mkdir -p "$VOL/.cache/pip" "$VOL/.cache/huggingface" "$VOL/data"

# Convenience tools
apt-get update -y
apt-get install -y git htop tmux curl build-essential

# Python venv
if [[ ! -d .venv ]]; then python3 -m venv .venv; fi
source .venv/bin/activate
python -m pip install --upgrade pip wheel

# Core libs
pip install -r requirements.txt

# Quick GPU sanity
nvidia-smi || true
python src/check_cuda.py || true
