"""R65 pure candidate and negative-regression tests; no forged literature facts."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r65_paragraph_provenance_candidate_audit.audit import (
    PINS, classify_candidate, classify_unreviewed_paragraphs, git_blob_sha,
    markdown_report, matching_projection_candidates, source_guard,
)


def sample_catalog() -> tuple[dict[str, object], ...]:
    return (
        {"step_index": 2, "projections": (("typed_sentence", "$E(x)=0$."),)},
        {"step_index": 3, "projections": (("body_latex", "$H(y)=z$"),)},
    )


def sample_ancestry() -> dict[int, dict[str, tuple[int, ...]]]:
    return {
        2: {"given_citations": (1,), "all_ancestor_citations": (1, 3)},
        3: {"given_citations": (2,), "all_ancestor_citations": (2,)},
    }


def test_exact_typed_projection_candidate_and_valid_given_ancestry() -> None:
    matches = matching_projection_candidates("[R1]より, $E(x)=0$.", sample_catalog())
    assert matches == ({"step_index": 2, "matched_by": ["typed_sentence"]},)
    assert classify_candidate((1,), matches, sample_ancestry()) == "UNIQUE_CANDIDATE_GIVEN_ANCESTOR_ELIGIBLE"


def test_other_ancestor_source_is_separate_from_given_source() -> None:
    match = matching_projection_candidates("[R3]を用いて, $E(x)=0$.", sample_catalog())
    assert classify_candidate((3,), match, sample_ancestry()) == "UNIQUE_CANDIDATE_OTHER_ANCESTOR_ELIGIBLE"


def test_unique_wrong_reference_is_not_certified() -> None:
    matches = matching_projection_candidates("[R2]より, $E(x)=0$.", sample_catalog())
    assert classify_candidate((2,), matches, sample_ancestry()) == "UNIQUE_CANDIDATE_TAG_NOT_IN_ANCESTRY"


def test_uncited_typed_projection_not_flagged_as_error() -> None:
    matches = matching_projection_candidates("$E(x)=0$.", sample_catalog())
    assert classify_candidate((), matches, sample_ancestry()) == "UNIQUE_CANDIDATE_UNCITED"


def test_ambiguous_typed_projection_not_certified() -> None:
    catalog = sample_catalog() + (
        {"step_index": 4, "projections": (("body_latex", "$E(x)=0$"),)},
    )
    matches = matching_projection_candidates("$E(x)=0$.", catalog)
    assert len(matches) == 2
    assert classify_candidate((1,), matches, sample_ancestry()) == "AMBIGUOUS_TYPED_WITNESS"


def test_unknown_projection_unmatched_and_no_implicit_source() -> None:
    assert matching_projection_candidates("ただし証明なし.", sample_catalog()) == ()
    assert classify_candidate((1,), (), sample_ancestry()) == "NO_LITERAL_TYPED_WITNESS"


def test_duplicate_catalog_step_fails_closed() -> None:
    catalog = sample_catalog() + (sample_catalog()[0],)
    with pytest.raises(RuntimeError, match="R65_DUPLICATE_CATALOG_STEP"):
        matching_projection_candidates("$E(x)=0$.", catalog)


@pytest.mark.parametrize("bad", [None, "", 4])
def test_bad_paragraph_rejected(bad) -> None:
    with pytest.raises(ValueError):
        matching_projection_candidates(bad, ())


def test_bad_catalog_rejected() -> None:
    with pytest.raises(TypeError):
        matching_projection_candidates("$E(x)=0$.", [])
    with pytest.raises(ValueError):
        matching_projection_candidates("$E(x)=0$.", ({"step_index": "2", "projections": ()},))
    with pytest.raises(ValueError):
        matching_projection_candidates("$E(x)=0$.", ({"step_index": 2, "projections": (("wrong", "abc"),)},))


def test_missing_ancestry_rejected() -> None:
    with pytest.raises(RuntimeError, match="R65_CANDIDATE_ANCESTRY_MISSING"):
        classify_candidate((1,), ({"step_index": 2, "matched_by": []},), {})


def test_bad_tag_rejected() -> None:
    with pytest.raises(ValueError):
        classify_candidate((0,), (), {})


def test_complete_unreviewed_inventory_preserved() -> None:
    inventory = {
        "sentence_relevance_not_yet_audited": 2,
        "lines": [
            {"attribution_review": "R63_TARGETED_ANCESTOR_ATTESTED", "text": "$x$"},
            {"attribution_review": "UNREVIEWED_SENTENCE_RELEVANCE", "text": "[R1]より, $E(x)=0$.", "citation_numbers": [1], "paragraph_number": 2, "priority": "P1_CITED_SENTENCE"},
            {"attribution_review": "UNREVIEWED_SENTENCE_RELEVANCE", "text": "説明.", "citation_numbers": [], "paragraph_number": 3, "priority": "P3_PROSE_OR_TRANSITION"},
        ],
    }
    result = classify_unreviewed_paragraphs(inventory, sample_catalog(), sample_ancestry())
    assert result["unreviewed_paragraphs"] == 2
    assert result["fully_certified_sentences_added"] == 0
    assert result["sentence_level_relevance_fully_proved"] is False
    assert {item["paragraph_number"] for item in result["records"]} == {2, 3}
    md = markdown_report({"sample": result})
    assert "段落 2" in md and "段落 3" in md
    assert "数学的な引用妥当性：未認定" in md


def test_count_drift_fails_closed() -> None:
    with pytest.raises(RuntimeError, match="R65_R64_UNREVIEWED_COUNT_DRIFT"):
        classify_unreviewed_paragraphs({"sentence_relevance_not_yet_audited": 1, "lines": []}, sample_catalog(), {})


def test_source_guard_pins_reviewed_repo() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(PINS) == 8
    assert source_guard(root) == tuple(PINS)


def test_source_guard_refuses_tamper_on_windows_or_posix(tmp_path: Path) -> None:
    relative = next(iter(PINS))
    destination = tmp_path / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(b"changed source")
    with pytest.raises(RuntimeError, match="R65_SOURCE_GUARD_FAILED"):
        source_guard(tmp_path)


def test_known_git_blob_sha() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
