"""R33 real-repository source, guard and typed frontier tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r33_three_premise_source_frontier.audit import (
    GIT_BLOB_PINS, LOCAL_SHA256_PINS, ROOT, SOURCE,
    canonical_sha256, inspect_registered_frontier, matches_blob_pin,
    report, verify_checkout,
)
from phase174_r3_r7_r33_three_premise_source_frontier.source_contract import (
    inspect_prior_three_clauses,
)


def test_source_guard_and_all_reviewed_pins() -> None:
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["r30_r31_r32_preserved"] is True
    assert len(GIT_BLOB_PINS) >= 10
    assert len(LOCAL_SHA256_PINS) == 4


def test_full_adopted_toda_has_independent_prior_clauses() -> None:
    text = (ROOT / SOURCE).read_text(encoding="utf-8-sig")
    refs = inspect_prior_three_clauses(text)
    assert len(refs) == 3
    assert all(not value.statement_is_verified_proof_step for value in refs)


def test_source_mutation_is_fail_closed() -> None:
    from phase174_r3_r7_r33_three_premise_source_frontier.source_contract import (
        IMAGE_CLAUSE,
    )
    text = (ROOT / SOURCE).read_text(encoding="utf-8-sig")
    with pytest.raises(ValueError):
        inspect_prior_three_clauses(text.replace(IMAGE_CLAUSE, "INVALID"))


def test_canonical_hash_rejects_arbitrary_changes() -> None:
    content = b"one\ntwo\n"
    assert canonical_sha256(content) == canonical_sha256(content.replace(b"\n", b"\r\n"))
    assert not matches_blob_pin(content, "0" * 40)


def test_screened_frontier_and_db_prior_are_not_proof() -> None:
    frontier = inspect_registered_frontier()
    assert frontier["strictly_earlier_db_prior_present"] is True
    assert frontier["db_prior_is_an_independent_literature_citation"] is False
    assert frontier["hypothetical_group_and_map_steps_not_certified"] is True
    assert frontier["kernel_direct_given_inserted"] is False
    assert frontier["root_direct_given_inserted"] is False
    assert frontier["db_prior_generator_type"]
    assert all(isinstance(frontier[key], int) for key in (
        "screened_domain_premises", "screened_codomain_premises",
        "screened_generator_image_premises",
    ))


def test_preflight_does_not_assert_completion() -> None:
    result = report(dry_run=True)
    assert result["gate"] == "PASS_R33_SOURCE_PREFLIGHT_ONLY"
    assert result["kernel_proved"] is False
    assert result["root_complete"] is False
    assert result["new_givens"] == 0
    assert result["new_inference_rules"] == 0
