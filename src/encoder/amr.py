"""AMR adapter scaffolding leveraging Penman/amrlib."""

from __future__ import annotations

from typing import Iterable, List


def load_parser(model_name: str = "amrlib-model-stog") -> object:
    """Instantiate an AMR parser with the requested checkpoint."""

    raise NotImplementedError


def parse_sentences(sentences: Iterable[str], parser: object) -> List[str]:
    """Return AMR graphs serialized in PENMAN notation."""

    raise NotImplementedError
