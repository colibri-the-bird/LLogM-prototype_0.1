"""Template for integrating AllenNLP SRL models into the pipeline."""

from __future__ import annotations

from typing import Iterable, List, Mapping


def load_model(model_name: str = "structured-pred-srl") -> object:
    """Return a lazily-initialized SRL predictor instance.

    Implementers should defer heavy imports until runtime and respect the cache locations defined
    in ``configs/global.yaml``.
    """

    raise NotImplementedError("Hook up AllenNLP SRL predictor here.")


def annotate(sentences: Iterable[str], model: object) -> List[Mapping[str, object]]:
    """Produce PropBank frames with roles and confidence scores."""

    raise NotImplementedError
