"""Frame Semantic Transformer adapter documentation stub."""

from __future__ import annotations

from typing import Iterable, List


def load_model(model_name: str = "frame-transformer-base") -> object:
    """Download or load the requested FST checkpoint and return a callable model."""

    raise NotImplementedError


def infer_frames(sentences: Iterable[str], model: object) -> List[dict]:
    """Return frame annotations compatible with the consolidation stage."""

    raise NotImplementedError
