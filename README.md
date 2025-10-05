# LLogM Prototype — RunPod bootstrap

Fast-start on a fresh RunPod GPU instance with reproducible configs.

## Quick start (RunPod pod, SSH inside)

```bash
# 1) Clone or create the repo under /workspace so it persists
cd /workspace
# git clone <your-remote> llogm  # or: mkdir llogm && cd llogm && git init

# 2) Put the files from this document into the repo (matching paths)

# 3) One-time: prepare env from example
cp .env.example .env
# Optional: edit .env with your own paths/tokens

# 4) Bootstrap
make setup        # creates venv, installs deps, pre-commit, etc.
make sanity       # GPU + torch check

# 5) Everyday workflow
# Option A: rely on RunPod template "Start Script" to call scripts/onstart.sh
# Option B: run it yourself after pod starts
make onstart
```

## Notes

* Keep the repo under `/workspace` so it survives Stop/Start.
* Configure your RunPod template env variables to match `configs/runpod.env`.
* If you use Accelerate, launch like this:

```bash
source .env
source .venv/bin/activate
accelerate launch --config_file configs/accelerate.yaml your_script.py
```
