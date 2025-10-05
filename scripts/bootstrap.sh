#!/usr/bin/env bash
set -euxo pipefail

# Prepare local development environment idempotently
[[ -f .env ]] || cp .env.example .env

make setup
