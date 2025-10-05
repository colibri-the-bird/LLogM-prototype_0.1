
SHELL := /bin/bash
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.DEFAULT_GOAL := help

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?##' Makefile | sort | awk 'BEGIN {FS := ":.*?## "}; {printf "[36m%-16s[0m %s
", $$1, $$2}'

setup: ## Create venv, install deps, setup pre-commit
	@test -d $(VENV) || python3 -m venv $(VENV)
	@echo "Activating venv and installing requirements..."
	@source $(VENV)/bin/activate && $(PIP) install --upgrade pip wheel
	@source $(VENV)/bin/activate && $(PIP) install -r requirements.txt
	@source $(VENV)/bin/activate && $(PIP) install pre-commit
	@pre-commit install || true

onstart: ## Run startup provisioning (idempotent)
	@bash scripts/onstart.sh

sanity: ## nvidia-smi + Torch CUDA check
	@bash scripts/sanity_checks.sh

hf-login: ## Hugging Face login (uses token if HF_TOKEN in .env)
	@source .env; source $(VENV)/bin/activate; \
	 if [[ -n "$$HF_TOKEN" ]]; then \
	   huggingface-cli login --token $$HF_TOKEN --add-to-git-credential; \
	 else \
	   echo "HF_TOKEN empty; running interactive login"; huggingface-cli login; \
	 fi

clean: ## Remove venv and caches (safe)
	rm -rf $(VENV)
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +

fmt: ## Run formatters and linters
	@pre-commit run --all-files || true

print-env: ## Show the effective env for debugging
	@bash scripts/print_env.sh
