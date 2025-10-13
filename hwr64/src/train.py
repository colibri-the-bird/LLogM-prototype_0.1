"""Minimal training entry point placeholder for HWR64."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HWR64 training stub")
    parser.add_argument("--config", type=Path, help="Path to training config", required=False)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.config:
        print(f"[HWR64] Training would start with config: {args.config}")
    else:
        print("[HWR64] No config provided. This is a placeholder training script.")


if __name__ == "__main__":
    main()
