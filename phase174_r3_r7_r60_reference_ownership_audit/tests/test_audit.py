"""Focused R60 tests: reference headings, source guard, and public proof links."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r60_reference_ownership_audit.audit import (
    PINS,
    audit_narrative_ownership,
    git_blob_sha,
    reference_heading_numbers,
    renderer_attribution_paths,
    source_guard,
)


def test_reference_headings_exclude_inline_tags() -> None:
    markdown = (
        "使用する結果\n\n**[R1] (5.1).**\n\n"
        "**[R2] Proposition 4.2.**\n\n"
        "証明\n\n[R1]より証明し, [R2]を用いる.\n"
    )
    assert reference_heading_numbers(markdown) == (1, 2)


@pytest.mark.parametrize("text", (
    "使用する結果\n\n", "[R3]より, 成り立つ.", "**[R1] first.** inline",
))
def test_reference_heading_parser_does_not_invent_other_numbers(text: str) -> None:
    assert all(number >= 1 for number in reference_heading_numbers(text))
    assert len(reference_heading_numbers(text)) <= 1


def test_heading_parser_rejects_non_string() -> None:
    with pytest.raises(TypeError):
        reference_heading_numbers(None)


def test_git_blob_sha_matches_known_git_blob() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"


def test_current_source_files_match_reviewed_git_blobs() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(PINS) == 6
    assert len(source_guard(root)) == 6


def test_common_renderer_still_contains_local_attribution_paths() -> None:
    root = Path(__file__).resolve().parents[2]
    assert renderer_attribution_paths(root) == (
        "cited_general_ancestor_numbers",
        "direct_given_premise_citation_numbers",
        "single_source_ancestor_numbers",
    )


def test_public_reference_ownership_and_both_complete_roots() -> None:
    root = Path(__file__).resolve().parents[2]
    from phase174_r3_r7_r60_reference_ownership_audit.audit import inspect_public
    reports = inspect_public(root)
    assert reports["pi11_6"]["reference_count"] == 7
    assert reports["pi12_7"]["reference_count"] == 3
    assert all(reports[key]["bidirectional_step_links"] for key in reports)
    assert all(reports[key]["no_outside_root_citation"] for key in reports)
    assert all(reports[key]["no_unowned_reference"] for key in reports)


def test_reference_ownership_refuses_noncomplete_proof_without_reclassification() -> None:
    # Minimal stub demonstrates that the audit cannot promote a partial proof.
    from phase165_r52_partial_proof import ProofSearchStatus

    class FakeResult:
        status = ProofSearchStatus.PARTIAL

    with pytest.raises(RuntimeError, match="not complete"):
        audit_narrative_ownership(FakeResult(), None, "")
