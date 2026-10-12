"""Phase 164 R4-R8: fixed literature references flow into actual reconstruction."""
from dataclasses import replace
from pathlib import Path

import pytest

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r8_registry_reconstruction import (
    _known_trusted_roots,
    reconstruct_phase164_r4_r8_pi5_3,
)
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaProp42ExactnessStatement


@pytest.fixture(scope="module")
def inputs():
    crosswalk = audit_current_repository(Path("phase163_r4_r94_output/manifest.json"))
    leaves = build_phase59_3_data()["premise_steps"]
    roots = _known_trusted_roots(leaves)
    return crosswalk, leaves, roots


def test_actual_registered_two_statements_reconstruct_pi5_3(inputs):
    crosswalk, leaves, roots = inputs
    result = reconstruct_phase164_r4_r8_pi5_3(
        crosswalk, leaves, roots, user_confirmed_original=True,
    )
    assert result.validated.reconstruction.final_step.conclusion == phase161_r5_target_goal()
    assert len(result.validated.reconstruction.derived_steps) == 7
    assert result.exactness_leaf_count == 4
    assert result.validated.provenance.verified_inferences >= 7


def test_registered_ids_are_real_and_limited(inputs):
    crosswalk, leaves, roots = inputs
    result = reconstruct_phase164_r4_r8_pi5_3(
        crosswalk, leaves, roots, user_confirmed_original=True,
    )
    assert result.cited_assertion_ids == (
        "toda:typed:ch5:prop5.1:finite_dimensional_subset",
        "toda:typed:ch5:eq5.3:hopf",
    )
    assert result.used_source_ids == ("toda:tex:ch5:0002", "toda:tex:ch5:0005")
    assert result.citation_mode == "confirmed_fixed_literature"


def test_user_confirmation_cannot_be_omitted(inputs):
    crosswalk, leaves, roots = inputs
    with pytest.raises(ValueError, match="explicit user"):
        reconstruct_phase164_r4_r8_pi5_3(
            crosswalk, leaves, roots, user_confirmed_original=False,
        )


def test_missing_trusted_root_rejected(inputs):
    crosswalk, leaves, roots = inputs
    with pytest.raises(ValueError, match="Untrusted GIVEN"):
        reconstruct_phase164_r4_r8_pi5_3(
            crosswalk, leaves, roots[1:], user_confirmed_original=True,
        )


def test_mutated_prop51_claim_rejected(inputs):
    crosswalk, leaves, roots = inputs
    old = leaves[0].conclusion
    delta = old.delta_iota5_relation
    changed_delta = replace(
        delta, positive_value=replace(delta.positive_value, coefficient=3),
    )
    changed_step = replace(leaves[0], conclusion=replace(old, delta_iota5_relation=changed_delta))
    with pytest.raises(ValueError, match="typed mathematical clause mismatch"):
        reconstruct_phase164_r4_r8_pi5_3(
            crosswalk, (changed_step,) + leaves[1:], roots,
            user_confirmed_original=True,
        )


def test_fake_source_statement_id_rejected(inputs):
    crosswalk, leaves, roots = inputs
    changed = dict(crosswalk)
    changed["leaves"] = [dict(row) for row in crosswalk["leaves"]]
    changed["leaves"][1]["source_statement_id"] = "toda:tex:ch5:fake"
    with pytest.raises(ValueError, match="source IDs or source identity changed"):
        reconstruct_phase164_r4_r8_pi5_3(
            changed, leaves, roots, user_confirmed_original=True,
        )


def test_missing_exactness_witness_rejected(inputs):
    crosswalk, leaves, roots = inputs
    with pytest.raises(ValueError, match="six distinct"):
        reconstruct_phase164_r4_r8_pi5_3(
            crosswalk, leaves[:-1], roots, user_confirmed_original=True,
        )


def test_duplicate_leaf_identity_rejected(inputs):
    crosswalk, leaves, roots = inputs
    with pytest.raises(ValueError, match="six distinct"):
        reconstruct_phase164_r4_r8_pi5_3(
            crosswalk, leaves[:-1] + (leaves[0],), roots,
            user_confirmed_original=True,
        )


def test_trusted_root_clone_rejected(inputs):
    crosswalk, leaves, roots = inputs
    altered = (replace(roots[0]),) + roots[1:]
    with pytest.raises(ValueError, match="Untrusted GIVEN"):
        reconstruct_phase164_r4_r8_pi5_3(
            crosswalk, leaves, altered, user_confirmed_original=True,
        )


def test_original_leaf_rules_remain_unchanged(inputs):
    crosswalk, leaves, roots = inputs
    before = tuple(id(s) for s in leaves)
    reconstruct_phase164_r4_r8_pi5_3(
        crosswalk, leaves, roots, user_confirmed_original=True,
    )
    assert tuple(id(s) for s in leaves) == before
    assert sum(s.rule is ProofRule.INFERENCE for s in leaves) == 2
    assert sum(s.rule is ProofRule.GIVEN and isinstance(s.conclusion, TodaProp42ExactnessStatement)
               for s in leaves) == 4
