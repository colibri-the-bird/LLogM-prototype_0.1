#!/usr/bin/env bash
set -euo pipefail

# This script documents the expected bootstrap flow. Replace the echo statements with
# concrete logic when wiring up the environment.

echo "[bootstrap] creating required directories..."
# mkdir -p data runs logs exports .cache

echo "[bootstrap] enabling git lfs tracking..."
# git lfs install
# git lfs track "exports/**" "data/raw/**"

echo "[bootstrap] installing pre-commit hooks..."
# pip install -r requirements-dev.txt
# pre-commit install

echo "[bootstrap] verifying Java availability..."
# java -version

echo "[bootstrap] collecting environment probe..."
# python scripts/utils/probe.py > exports/bootstrap_report.json

echo "[bootstrap] complete. Review the TODO markers inside this script to enable each step."
