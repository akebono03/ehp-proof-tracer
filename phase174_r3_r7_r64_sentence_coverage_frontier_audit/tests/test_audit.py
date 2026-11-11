"""Focused isolated R64 coverage inventory and failure-closed controls."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r64_sentence_coverage_frontier_audit.audit import (
    PINS, audited_line_inventory, git_blob_sha, priority_of_untested_line,
    proof_body_lines, source_guard,
)


def sample_markdown() -> str:
    return (
        "使用する結果\n\n**[R1] Example.**\n\n$x=y$.\n\n証明\n\n"
        "[R1]より, $x=y$.\n\n"
        "$z=w$.\n\n"
        "以上より, $A=B$.\n\n□\n"
    )


def test_full_line_inventory_is_conservative() -> None:
    result = audited_line_inventory(
        sample_markdown(), (1,), {"given": {"proof_line": "[R1]より, $x=y$."}}
    )
    assert result["total_proof_paragraphs"] == 3
    assert result["r63_targeted_paragraphs"] == 1
    assert result["sentence_relevance_not_yet_audited"] == 2
    assert result["full_sentence_attribution_audited"] is False
    assert result["lines"][1]["attribution_review"] == "UNREVIEWED_SENTENCE_RELEVANCE"
    assert result["lines"][2]["priority"] == "P1_UNCITED_INFERENCE"


def test_reference_paragraphs_not_counted_as_proof() -> None:
    assert proof_body_lines(sample_markdown()) == (
        "[R1]より, $x=y$.", "$z=w$.", "以上より, $A=B$."
    )


@pytest.mark.parametrize("value", [None, "", "証明\n\n[R1]よりx\n□", "使用する結果\n\n証明\n", "使用する結果\n証明\n証明\n□"])
def test_missing_or_ambiguous_proof_boundary_rejected(value) -> None:
    with pytest.raises((TypeError, RuntimeError)):
        proof_body_lines(value)


def test_unknown_rendered_tag_is_rejected() -> None:
    changed = sample_markdown().replace("[R1]より", "[R2]より")
    with pytest.raises(RuntimeError, match="UNKNOWN_RENDERED_CITATION"):
        audited_line_inventory(changed, (1,), {"given": {"proof_line": "[R2]より, $x=y$."}})


def test_duplicate_r63_witness_sentence_rejected() -> None:
    sentence = "[R1]より, $x=y$."
    with pytest.raises(RuntimeError, match="DUPLICATE_R63_WITNESS_LINE"):
        audited_line_inventory(sample_markdown(), (1,), {
            "first": {"proof_line": sentence}, "second": {"proof_line": sentence},
        })


def test_r63_target_line_must_exist_exactly() -> None:
    with pytest.raises(RuntimeError, match="R63_TARGET_LINES_NOT_ALL_RENDERED"):
        audited_line_inventory(sample_markdown(), (1,), {
            "given": {"proof_line": "[R1]より, $x=wrong$."},
        })


def test_r63_target_line_must_not_repeat() -> None:
    duplicated = sample_markdown().replace("$z=w$.", "[R1]より, $x=y$.")
    with pytest.raises(RuntimeError, match="AMBIGUOUS_TARGETED_LINE"):
        audited_line_inventory(duplicated, (1,), {
            "given": {"proof_line": "[R1]より, $x=y$."},
        })


def test_unverified_citation_does_not_become_certified() -> None:
    changed = sample_markdown().replace("$z=w$.", "[R1]より, $z=w$.")
    report = audited_line_inventory(changed, (1,), {
        "given": {"proof_line": "[R1]より, $x=y$."},
    })
    assert report["lines"][1]["priority"] == "P1_CITED_SENTENCE"
    assert report["lines"][1]["attribution_review"] == "UNREVIEWED_SENTENCE_RELEVANCE"


def test_no_citation_is_not_an_automatic_defect() -> None:
    assert priority_of_untested_line("$x=y$.", ()) == "P2_MATH_WITHOUT_INLINE_TAG"
    assert priority_of_untested_line("説明の続き.", ()) == "P3_PROSE_OR_TRANSITION"


def test_invalid_citation_number_tuple_rejected() -> None:
    for values in ((2,), (1, 3), (1, 1), [1], ("1",)):
        with pytest.raises(ValueError):
            audited_line_inventory(sample_markdown(), values, {"given": {"proof_line": "[R1]より, $x=y$."}})


def test_empty_or_untyped_witness_rejected() -> None:
    for targets in ({}, {"x": {"proof_line": ""}}, {"x": object()}):
        with pytest.raises(ValueError):
            audited_line_inventory(sample_markdown(), (1,), targets)


def test_readonly_source_pin_contract() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(PINS) == 8
    assert source_guard(root) == tuple(PINS)


def test_source_guard_rejects_tamper(tmp_path: Path) -> None:
    relative = next(iter(PINS))
    target = tmp_path / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"unreviewed")
    with pytest.raises(RuntimeError, match="R64_SOURCE_BLOB_MISMATCH"):
        source_guard(tmp_path)


def test_git_blob_fixture() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
