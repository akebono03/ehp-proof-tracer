"""R69 pure control tests. Real Proof Tree inspection is run by run.ps1."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r69_general_narrative_gap_audit.audit import (
    PINS, decide_composite_display, decide_presentation_boundary,
    git_blob_sha, source_guard, step_index,
)


def test_four_premise_root_does_not_certify_intermediate_steps() -> None:
    assert decide_presentation_boundary(
        root_verified=True, explicit_zero_e=False,
        explicit_h_injective=False,
    ) == "FOUR_PREMISE_ROOT_VERIFIED_INTERMEDIATE_STEPS_NOT_ALL_EXPLICIT"


def test_only_both_explicit_steps_admit_explicit_label() -> None:
    assert decide_presentation_boundary(
        root_verified=True, explicit_zero_e=True,
        explicit_h_injective=True,
    ) == "EXPLICIT_INTERMEDIATE_PROOFSTEPS_PRESENT"
    assert decide_presentation_boundary(
        root_verified=True, explicit_zero_e=True,
        explicit_h_injective=False,
    ) != "EXPLICIT_INTERMEDIATE_PROOFSTEPS_PRESENT"


def test_unverified_root_is_not_certified() -> None:
    assert decide_presentation_boundary(
        root_verified=False, explicit_zero_e=True,
        explicit_h_injective=True,
    ) == "ROOT_NOT_VERIFIED"


@pytest.mark.parametrize("invalid", [None, 1, "True"])
def test_invalid_root_status_rejected(invalid) -> None:
    with pytest.raises(TypeError):
        decide_presentation_boundary(
            root_verified=invalid, explicit_zero_e=True,
            explicit_h_injective=True,
        )


def test_composite_requires_all_typed_witness_roles() -> None:
    assert decide_composite_display(
        generator_zero_step=True, r2_cited_given_ancestor=True,
        component_images_verified=True,
    ) == "CANDIDATE_CHAIN_NEEDS_GENERIC_RENDERING_REVIEW"
    assert decide_composite_display(
        generator_zero_step=True, r2_cited_given_ancestor=False,
        component_images_verified=True,
    ) == "INCOMPLETE_WITNESS_FOR_PROPOSED_CONDENSED_SENTENCE"


@pytest.mark.parametrize("invalid", [None, 1, "true"])
def test_bad_composite_flags_rejected(invalid) -> None:
    with pytest.raises(TypeError):
        decide_composite_display(
            generator_zero_step=True, r2_cited_given_ancestor=invalid,
            component_images_verified=True,
        )


def test_premise_identity_wins() -> None:
    original = SimpleNamespace(value="A")
    model = SimpleNamespace(steps=(original, SimpleNamespace(value="B")))
    assert step_index(model, original) == 0


def test_equal_but_unique_premise_may_be_found() -> None:
    model = SimpleNamespace(steps=(SimpleNamespace(value="A"),))
    assert step_index(model, SimpleNamespace(value="A")) == 0


def test_missing_premise_fails_closed() -> None:
    model = SimpleNamespace(steps=(SimpleNamespace(value="A"),))
    with pytest.raises(RuntimeError, match="R69_MISSING_OR_AMBIGUOUS_PREMISE"):
        step_index(model, SimpleNamespace(value="B"))


def test_ambiguous_premise_fails_closed() -> None:
    model = SimpleNamespace(steps=(SimpleNamespace(value="A"), SimpleNamespace(value="A")))
    with pytest.raises(RuntimeError, match="R69_MISSING_OR_AMBIGUOUS_PREMISE"):
        step_index(model, SimpleNamespace(value="A"))


def test_source_guard_pins_reviewed_repo() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(PINS) == 8
    assert source_guard(root) == tuple(PINS)


def test_source_guard_rejects_modified_blob(tmp_path: Path) -> None:
    relative = next(iter(PINS))
    dest = tmp_path / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(b"wrong")
    with pytest.raises(RuntimeError, match="R69_REVIEWED_SOURCE_MISMATCH"):
        source_guard(tmp_path)


def test_known_git_blob_identity() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
