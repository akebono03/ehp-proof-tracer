"""Focused live-repository checks against the R15R4 actually replayed frontier."""
from __future__ import annotations

from pathlib import Path

from phase173_r4_r15r5_family_source_frontier.audit import (
    inspect_family_source_frontier,
)


ROOT = Path(__file__).resolve().parents[2]


def test_k31_source_frontier_preserves_three_unproved_pairs() -> None:
    row = inspect_family_source_frontier(ROOT, k=31)
    assert row["named_image_candidates"] == 4
    assert row["named_images_replayed"] == 1
    assert len(row["unresolved_pairs"]) == 3
    assert row["unresolved_family_ids"] == [56, 88]
    assert all(not pair["proof_engine_replayed"] for pair in row["unresolved_pairs"])
    assert row["new_given_created"] is False
    assert row["public_completion"] is False


def test_family_56_and_88_metadata_are_not_promoted_to_citations() -> None:
    row = inspect_family_source_frontier(ROOT, k=31)
    assert {entry["family_id"] for entry in row["family_sources"]} == {56, 88}
    for entry in row["family_sources"]:
        assert entry["minimum_n"] >= 2
        assert entry["stem"] >= 0
        assert entry["cited_family_definition_available"] is False
        assert entry["source_definition_certified"] is False
        assert entry["new_given_created"] is False
        assert entry["source_files"]
        assert all(hit["source_reviewed"] is False
                   for hit in entry["candidate_text_hits"])
