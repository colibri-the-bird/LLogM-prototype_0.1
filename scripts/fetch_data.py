"""Data bootstrapper for public datasets referenced in configs/datasets.yaml."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True, help="Dataset catalog configuration")
    parser.add_argument("--max-workers", type=int, default=4, help="Parallel download workers")
    parser.add_argument("--output", type=Path, default=Path("data"), help="Root directory for datasets")
    return parser


def main(args: argparse.Namespace) -> None:
    """Inspect the dataset catalog and download/convert each enabled entry."""

    raise NotImplementedError("Implement dataset fetching, checksum validation, and manifest writing.")


if __name__ == "__main__":
    main(build_arg_parser().parse_args())
