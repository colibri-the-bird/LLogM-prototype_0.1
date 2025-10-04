# LLogM-prototype_0.1

This repository packages the environment and bootstrap guide for the first LLogM prototype.
It focuses on reproducible setup steps, configuration templates, and orchestration scaffolding
for transforming raw text into a consolidated **C-Graph** (concepts, events, roles, relations).

The repository intentionally ships **instructions and file templates** instead of full
implementations so that downstream teams or agents can complete the missing logic while keeping
interfaces consistent.

## Quick start

1. Copy `.env.example` to `.env` and update the cache paths and service ports.
2. Follow `scripts/bootstrap.sh` to prepare the working directories, install developer tooling,
   and record the environment probe to `exports/bootstrap_report.json`.
3. Use `scripts/pull_models.py --fast` to prefetch the lightweight model set for smoke tests.
4. Launch supporting services (OpenIE5, HeidelTime) via `docker/compose.yaml`.
5. Run `scripts/run_encoder.py` to execute the text → C-Graph pipeline. Sample commands and
   configuration overrides are included inside the script.

Refer to the individual configuration files in `configs/` for the default stack and dataset
selections. Each adapter within `src/encoder/` provides structured docstrings describing the
expected behaviour and payload formats.

CI, formatting, and linting guidance is provided through `.pre-commit-config.yaml` and
`.github/workflows/ci.yml`. Update both when adding new tooling or tests.
