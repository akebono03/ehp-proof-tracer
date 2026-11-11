"""Focused boundary tests; simulated records never become mathematical facts."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r66_verified_paragraph_boundary_audit.audit import (
    EXPECTED, PINS, git_blob_sha, markdown_report, source_guard,
    validate_frontier_record,
)


def fake_record(status: str, *, tags: list[int], candidates: list[dict[str, object]],
                text: str = "$E(x)=0$." ) -> dict[str, object]:
    return {
        "paragraph_number": 4, "text": text,
        "reference_tags": tags, "candidate_steps": candidates,
        "candidate_status": status,
    }


def fake_step_details() -> dict[int, dict[str, object]]:
    return {5: {
        "step_index": 5, "step_rule": "INFERENCE", "ancestor_indices": (1, 5),
        "given_ancestor_references": (2,), "all_ancestor_references": (2, 3),
        "own_references": (),
    }}


def candidate() -> dict[str, object]:
    return {
        "step_index": 5, "matching_projections": ["typed_sentence"],
        "given_ancestor_references": [2],
        "all_ancestor_references": [2, 3],
    }


def test_cited_projection_requires_real_given_ancestor() -> None:
    record = fake_record("UNIQUE_CANDIDATE_GIVEN_ANCESTOR_ELIGIBLE",
                         tags=[2], candidates=[candidate()])
    result = validate_frontier_record(record, frozenset({1, 5}), fake_step_details(), {})
    assert result["verification_boundary"] == "CITED_TYPED_PROJECTION_WITH_GIVEN_ANCESTRY"
    assert result["given_ancestor_references"] == [2]
    assert result["sentence_level_semantic_relevance_proved"] is False


def test_wrong_citation_rejected_not_promoted() -> None:
    record = fake_record("UNIQUE_CANDIDATE_GIVEN_ANCESTOR_ELIGIBLE",
                         tags=[3], candidates=[candidate()])
    with pytest.raises(RuntimeError, match="R66_TAG_NOT_OWNED_BY_GIVEN_ANCESTRY"):
        validate_frontier_record(record, frozenset({1, 5}), fake_step_details(), {})


def test_uncited_projection_has_proof_step_not_forced_citation() -> None:
    record = fake_record("UNIQUE_CANDIDATE_UNCITED", tags=[], candidates=[candidate()])
    result = validate_frontier_record(record, frozenset({1, 5}), fake_step_details(), {})
    assert result["verification_boundary"] == "UNCITED_TYPED_PROJECTION_WITH_VERIFIED_STEP"
    assert result["reference_tags"] == []


def test_citation_added_to_uncited_record_rejected() -> None:
    record = fake_record("UNIQUE_CANDIDATE_UNCITED", tags=[2], candidates=[candidate()])
    with pytest.raises(RuntimeError, match="R66_UNCITED_PARAGRAPH_HAS_REFERENCE_TAG"):
        validate_frontier_record(record, frozenset({1, 5}), fake_step_details(), {})


def test_nonliteral_verified_exactness_line_is_structurally_bound() -> None:
    text = r"$\pi_3^2 \xrightarrow{E} \pi_4^3$."
    record = fake_record("NO_LITERAL_TYPED_WITNESS", tags=[], candidates=[], text=text)
    result = validate_frontier_record(record, frozenset({1, 5}), {}, {text: (1, 5)})
    assert result["verification_boundary"] == "CERTIFIED_EXACTNESS_CHAIN_DISPLAY"
    assert result["certified_chain_step_indices"] == [1, 5]


def test_nonliteral_text_is_not_certified_without_exact_chain() -> None:
    record = fake_record("NO_LITERAL_TYPED_WITNESS", tags=[], candidates=[],
                         text="以上より群構造を決定する.")
    result = validate_frontier_record(record, frozenset({1, 5}), {}, {})
    assert result["verification_boundary"] == "NO_LITERAL_STEP_OR_CHAIN_WITNESS"


def test_exactness_line_outside_root_rejected() -> None:
    text = "$A\\to B$."
    record = fake_record("NO_LITERAL_TYPED_WITNESS", tags=[], candidates=[], text=text)
    with pytest.raises(RuntimeError, match="R66_CHAIN_OUTSIDE_CERTIFIED_ROOT"):
        validate_frontier_record(record, frozenset({1}), {}, {text: (2,)})


def test_nonliteral_cannot_have_forged_typed_candidate() -> None:
    record = fake_record("NO_LITERAL_TYPED_WITNESS", tags=[], candidates=[candidate()])
    with pytest.raises(RuntimeError, match="R66_UNEXPECTED_NONLITERAL_CANDIDATE"):
        validate_frontier_record(record, frozenset({1, 5}), fake_step_details(), {})


def test_outside_root_candidate_rejected() -> None:
    record = fake_record("UNIQUE_CANDIDATE_UNCITED", tags=[], candidates=[candidate()])
    with pytest.raises(RuntimeError, match="R66_CANDIDATE_OUTSIDE_VERIFIED_ROOT"):
        validate_frontier_record(record, frozenset({1}), fake_step_details(), {})


def test_recorded_ancestry_disagreement_rejected() -> None:
    wrong = candidate()
    wrong["all_ancestor_references"] = [99]
    record = fake_record("UNIQUE_CANDIDATE_UNCITED", tags=[], candidates=[wrong])
    with pytest.raises(RuntimeError, match="R66_RECORDED_ANCESTRY_DISAGREES_WITH_PROOF_TREE"):
        validate_frontier_record(record, frozenset({1, 5}), fake_step_details(), {})


def test_ambiguous_candidate_rejected() -> None:
    record = fake_record("UNIQUE_CANDIDATE_UNCITED", tags=[],
                         candidates=[candidate(), candidate()])
    with pytest.raises(RuntimeError, match="R66_UNIQUE_CANDIDATE_REQUIRED"):
        validate_frontier_record(record, frozenset({1, 5}), fake_step_details(), {})


def test_new_unexpected_classification_fails_closed() -> None:
    record = fake_record("AMBIGUOUS_TYPED_WITNESS", tags=[], candidates=[candidate()])
    with pytest.raises(RuntimeError, match="R66_NEW_UNREVIEWED_CLASSIFICATION"):
        validate_frontier_record(record, frozenset({1, 5}), fake_step_details(), {})


@pytest.mark.parametrize("bad", [0, None, "4"])
def test_invalid_paragraph_index_rejected(bad) -> None:
    record = fake_record("NO_LITERAL_TYPED_WITNESS", tags=[], candidates=[])
    record["paragraph_number"] = bad
    with pytest.raises(ValueError, match="R66_INVALID_FRONTIER_RECORD"):
        validate_frontier_record(record, frozenset(), {}, {})


def test_focused_frontier_counts_match_user_confirmed_r65() -> None:
    assert EXPECTED["pi11_6"]["unreviewed"] == 11
    assert EXPECTED["pi12_7"]["unreviewed"] == 4
    assert sum(x["NO_LITERAL_TYPED_WITNESS"] for x in EXPECTED.values()) == 2
    assert sum(x["UNIQUE_CANDIDATE_UNCITED"] for x in EXPECTED.values()) == 7
    assert sum(x["UNIQUE_CANDIDATE_GIVEN_ANCESTOR_ELIGIBLE"] for x in EXPECTED.values()) == 6


def test_markdown_report_preserves_full_text_and_uncertainty() -> None:
    text = "以上より, $A=0$."
    sample = {"sample": {"unreviewed_paragraphs": 1, "records": [{
        "paragraph_number": 2, "text": text, "reference_tags": [],
        "verification_boundary": "NO_LITERAL_STEP_OR_CHAIN_WITNESS",
    }]}}
    rendered = markdown_report(sample)
    assert text in rendered
    assert "未認定" in rendered


def test_source_guard_rejects_tamper(tmp_path: Path) -> None:
    relative = next(iter(PINS))
    dest = tmp_path / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(b"changed")
    with pytest.raises(RuntimeError, match="R66_REVIEWED_BLOB_MISMATCH"):
        source_guard(tmp_path)


def test_source_guard_accepts_reviewed_repo() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(PINS) == 9
    assert source_guard(root) == tuple(PINS)


def test_known_blob_identity() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
