"""Guidelines for consolidating adapter outputs into the C-Graph schema."""

from __future__ import annotations

from typing import Dict, List


class ConsolidationError(RuntimeError):
    """Raised when ontology constraints cannot be satisfied during consolidation."""


def consolidate(document_payload: Dict[str, object]) -> Dict[str, object]:
    """Merge entities, events, and relations into the normalized C-Graph representation.

    Implementers should:

    * Canonicalize entity identifiers using coreference clusters.
    * Normalize role labels to the ontology inventory.
    * Resolve conflicting temporal relations while respecting transitivity constraints.
    * Preserve provenance metadata for downstream auditing.
    """

    raise NotImplementedError
