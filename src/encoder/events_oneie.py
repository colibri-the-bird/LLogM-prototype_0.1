"""Event extraction adapter outlines for OneIE / DyGIE++ style models."""

from __future__ import annotations

from typing import Iterable, List, Mapping


class EventExtractor:
    """Lightweight wrapper capturing the differences between OneIE and DyGIE++ backends."""

    def __init__(self, backend: str) -> None:
        self.backend = backend

    def load(self) -> None:
        """Populate runtime attributes such as tokenizers and model weights."""

        raise NotImplementedError

    def predict(self, sentences: Iterable[str]) -> List[Mapping[str, object]]:
        """Return structured event records with triggers, arguments, and scores."""

        raise NotImplementedError
