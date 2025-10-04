"""Prefetch model weights listed in the encoder stack configuration."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict


def build_arg_parser() -> argparse.ArgumentParser:
    """Return the CLI parser for the model puller."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True, help="Path to encoder_stack.yaml")
    parser.add_argument("--fast", action="store_true", help="Limit downloads to lightweight models")
    parser.add_argument("--offline", action="store_true", help="Avoid network access and only verify caches")
    parser.add_argument("--output", type=Path, default=Path("exports/models_report.json"))
    return parser


def main(args: argparse.Namespace) -> None:
    """Load configuration and fetch the associated Hugging Face or local models."""

    raise NotImplementedError("Implement model discovery, download, and reporting.")


if __name__ == "__main__":
    main(build_arg_parser().parse_args())
