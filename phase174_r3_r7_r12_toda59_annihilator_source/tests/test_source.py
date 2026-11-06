"""Focused adopted-text boundary and source-only metadata tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    CitedFamilyAnnihilator, PROPOSITION_START, SOURCE_ANNIHILATOR_LOCATOR,
    TODA_CLAUSE, verify_toda59_annihilator_text,
)


def example_source() -> str:
    return (
        "before\n" + PROPOSITION_START + "\n"
        + r"\textbf{(5.9).}" + "\n"
        + TODA_CLAUSE + "\n"
        + r"E\pi_{10}^5=0" + "\n"
        + r"\qed" + "\n"
    )


def test_exact_general_citation_is_source_metadata_not_proof(tmp_path: Path) -> None:
    path = tmp_path / "toda.tex"
    path.write_text(example_source(), encoding="utf-8")
    result = verify_toda59_annihilator_text(path)
    assert result["source_not_registered_as_given"] is True
    assert result["printed_edition_independently_verified"] is False
    assert result["general_relation"] == TODA_CLAUSE
    assert result["relative_position"] < result["direct_image_zero_position"]


@pytest.mark.parametrize("mutator", (
    lambda s: s.replace(TODA_CLAUSE, ""),
    lambda s: s.replace(TODA_CLAUSE, TODA_CLAUSE + "\n" + TODA_CLAUSE),
    lambda s: s.replace("n\\ge6", "n\\ge5"),
    lambda s: s.replace(r"\textbf{(5.9).}", ""),
    lambda s: s.replace(PROPOSITION_START, ""),
    lambda s: s.replace(r"\qed", ""),
    lambda s: s.replace(TODA_CLAUSE, "PLACEHOLDER").replace(r"E\pi_{10}^5=0", TODA_CLAUSE).replace("PLACEHOLDER", r"E\pi_{10}^5=0"),
))
def test_modified_or_unpositioned_source_is_rejected(tmp_path: Path, mutator) -> None:
    path = tmp_path / "toda.tex"
    path.write_text(mutator(example_source()), encoding="utf-8")
    with pytest.raises(RuntimeError):
        verify_toda59_annihilator_text(path)


def test_general_schema_is_distinct_from_target_group_statement() -> None:
    claim = CitedFamilyAnnihilator(4, 2, 6, 3, SOURCE_ANNIHILATOR_LOCATOR)
    assert claim.left_family_id != claim.right_family_id
    assert claim.right_index_offset == 3
    assert claim.minimum_left_index == 6
    assert "Proposition 5.9" in claim.citation_locator
