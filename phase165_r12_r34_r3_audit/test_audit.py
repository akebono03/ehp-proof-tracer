"""Targeted provenance checks only."""
from __future__ import annotations

from audit import audit


def test_r3_generator_suspension_is_iota1_to_iota2() -> None:
    result = audit()
    assert result["statement"] == "E(ι₁)=ι₂"
    assert result["source_generator"] == "ι₁"
    assert result["target_generator"] == "ι₂"


def test_r3_foundational_given_keeps_provenance() -> None:
    result = audit()
    assert result["rule"] == "GIVEN"
    assert result["foundational_reference"] == "foundational:suspension-identity"
    assert result["provenance_attached_to_constructed_leaf"] is True
    assert result["actual_pi43_proof_tree_checked"] is False
