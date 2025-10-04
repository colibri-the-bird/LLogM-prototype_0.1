# C-Graph Base Schema

This document summarizes the canonical structure that consolidated documents should follow.
It is a companion to ``configs/ontology.yaml`` and informs the implementation of
``src/encoder/consolidate.py``.

## Top-level keys

- ``doc_id``: unique identifier mirroring the source document.
- ``entities``: list of entity records containing ``id``, ``text``, optional ``kb`` links, and type.
- ``events``: list of events with ``id``, ``type``, ``args`` (role → entity/event), and optional time.
- ``relations``: triples of ``[relation_name, source_id, target_id]``.
- ``times``: temporal anchors normalized to ISO 8601 when possible.
- ``provenance``: array of backend-specific traces, each capturing ``source_backend``, ``score``,
  and text offsets.
- ``conflicts``: optional diagnostics when ontology axioms cannot be fully enforced.

## Provenance records

Each provenance entry should minimally include:

```json
{
  "backend": "openie5",
  "confidence": 0.82,
  "span": [15, 24],
  "notes": "subject/object swapped during normalization"
}
```

## Constraints

- Temporal edges (``BEFORE``, ``AFTER``) must respect irreflexivity and avoid cycles.
- ``IS_A`` and ``PART_OF`` should never emit duplicate inverse pairs because both are
  antisymmetric.
- Conflicting relations should be resolved using backend confidence scores or predefined
  precedence rules.

## Recommended file layout

C-Graph exports should live under ``exports/cgraph/`` and use either ``.json`` or ``.jsonl``
depending on batch size. Maintain a manifest in ``exports/manifest.json`` describing the run
configuration, timestamp, and source command line.
