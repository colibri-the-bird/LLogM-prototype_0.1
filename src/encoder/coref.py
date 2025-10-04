"""Coreference adapter template for fastcoref or neuralcoref backends."""

from __future__ import annotations

from typing import Iterable, List


def resolve_coref(sentences: Iterable[str], backend: str = "fastcoref") -> List[dict]:
    """Return clusters and mention metadata for subsequent consolidation."""

    raise NotImplementedError
