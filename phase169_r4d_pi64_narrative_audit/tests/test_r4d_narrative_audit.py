"""R4D formatting checks only: no synthetic proof assertions."""
from __future__ import annotations

from phase169_r4d_pi64_narrative_audit.checks import (
    citation_usage,
    split_narrative,
    visual_findings,
)


def test_r4d_reference_and_proof_split():
    reference, body = split_narrative(
        "使用する結果\n\n**[R1] Proposition 4.4.**\n証明\n[R1]より, $E$ は単射.\n□\n"
    )
    assert "Proposition 4.4" in reference
    assert body.rstrip().endswith("□")


def test_r4d_exact_citation_numbers_not_display_labels():
    markdown = "使用する結果\n\n**[R1] X.**\n**[R2] Y.**\n証明\n[R2]を用いる.\n□\n"
    usage = citation_usage(markdown, (1, 2))
    assert usage["heading_count_matches"] is True
    assert usage["uncited_in_proof"] == [1]
    assert usage["unknown_in_proof"] == []


def test_r4d_unregistered_body_citation_flagged():
    markdown = "使用する結果\n\n**[R1] X.**\n証明\n[R9]を用いる.\n□\n"
    usage = citation_usage(markdown, (1,))
    findings = visual_findings(markdown, usage)
    assert usage["unknown_in_proof"] == [9]
    assert "UNKNOWN_REFERENCE_TAG_IN_BODY" in findings


def test_r4d_incomplete_label_and_missing_qed_flagged():
    markdown = "使用する結果\n\n証明\n部分証明・未完成\n"
    usage = citation_usage(markdown, ())
    findings = visual_findings(markdown, usage)
    assert "INCOMPLETE_PROOF_LABEL_IN_COMPLETE_NARRATIVE" in findings
    assert "NO_FINAL_PROOF_SYMBOL" in findings
