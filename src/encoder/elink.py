"""Entity linking adapter placeholders for BLINK/REL/GLiNER."""

from __future__ import annotations

from typing import Iterable, List


def link_entities(mentions: Iterable[dict], backend: str = "blink") -> List[dict]:
    """Resolve entity mentions to knowledge base identifiers using the requested backend."""

    raise NotImplementedError
