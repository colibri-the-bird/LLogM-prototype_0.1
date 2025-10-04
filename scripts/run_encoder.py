"""CLI entrypoint for the text → C-Graph encoding pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterator, Optional

from src.encoder import pipeline


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack", type=Path, required=True, help="Encoder stack configuration")
    parser.add_argument("--runtime", type=Path, help="Optional runtime configuration")
    parser.add_argument("--in", dest="input_path", type=Path, help="Input JSONL file; omit for stdin")
    parser.add_argument("--out", dest="output_path", type=Path, required=True, help="Output path for C-Graphs")
    parser.add_argument("--override", action="append", help="Configuration overrides components.foo.enabled=false")
    parser.add_argument("--offline", action="store_true", help="Skip network calls and rely on caches only")
    parser.add_argument("--num-workers", type=int, default=1, help="Future parallelism knob (unused template)")
    return parser


def iter_documents(input_path: Optional[Path]) -> Iterator[dict]:
    """Yield documents from stdin or a JSONL file."""

    if input_path is None:
        for line in sys.stdin:
            if line.strip():
                yield json.loads(line)
        return

    with input_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def main(args: argparse.Namespace) -> None:
    config = pipeline.PipelineConfig(
        stack_config=args.stack,
        runtime_config=args.runtime,
        overrides=args.override,
        input_path=args.input_path,
        output_path=args.output_path,
        offline=args.offline,
    )

    resolved = pipeline.load_configs(config)
    graphs = pipeline.run_pipeline(iter_documents(args.input_path), resolved)
    pipeline.save_outputs(graphs, args.output_path)


if __name__ == "__main__":
    main(build_arg_parser().parse_args())
