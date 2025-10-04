"""Schema compatibility checks for ontology relations."""

import pytest


@pytest.mark.skip(reason="Ontology validation pending implementation")
def test_relations_exist_in_ontology() -> None:
    """Ensure every relation emitted by adapters is present in configs/ontology.yaml."""

    raise NotImplementedError
