"""Focused Phase 161 R7 provenance boundary tests."""

from dataclasses import replace

import pytest

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import (
    reconstruct_phase161_r7_validated_goal,
    validate_phase161_r7_provenance,
)
from proof import ProofRule, ProofStep
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data


def _fixture():
    leaves = build_phase59_3_data()["premise_steps"]
    roots = {}
    seen = set()

    def walk(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        if step.rule is ProofRule.GIVEN:
            roots[id(step)] = step
        for premise in step.premises:
            walk(premise)

    for leaf in leaves:
        walk(leaf)
    return leaves, tuple(roots.values())


def test_phase161_r7_valid_reconstruction_has_verified_ancestry():
    leaves, trusted = _fixture()
    result = reconstruct_phase161_r7_validated_goal(
        phase161_r5_target_goal(), leaves, trusted
    )
    assert result.reconstruction.final_step.conclusion == phase161_r5_target_goal()
    assert len(result.reconstruction.derived_steps) == 7
    assert result.provenance.verified_inferences >= 7
    assert len(result.provenance.trusted_roots_used) >= 4


def test_phase161_r7_rejects_missing_inference_ancestry():
    leaves, trusted = _fixture()
    literature = next(step for step in leaves if step.rule is ProofRule.INFERENCE)
    corrupted = replace(literature, premises=())
    modified = tuple(corrupted if step is literature else step for step in leaves)
    with pytest.raises(ValueError, match="Unjustified INFERENCE ancestry"):
        reconstruct_phase161_r7_validated_goal(
            phase161_r5_target_goal(), modified, trusted
        )


def test_phase161_r7_rejects_untrusted_exactness_given():
    leaves, trusted = _fixture()
    exactness = next(step for step in leaves if step.rule is ProofRule.GIVEN)
    restricted = tuple(step for step in trusted if step is not exactness)
    with pytest.raises(ValueError, match="Untrusted GIVEN provenance root"):
        reconstruct_phase161_r7_validated_goal(
            phase161_r5_target_goal(), leaves, restricted
        )


def test_phase161_r7_rejects_tampered_inference_conclusion():
    leaves, trusted = _fixture()
    literature = next(step for step in leaves if step.rule is ProofRule.INFERENCE)
    tampered = replace(literature, conclusion=object())
    modified = tuple(tampered if step is literature else step for step in leaves)
    with pytest.raises(ValueError, match="Inference does not follow from recorded premises"):
        validate_phase161_r7_provenance(modified, trusted)


def test_phase161_r7_requires_same_trusted_object_identity():
    leaves, trusted = _fixture()
    exactness = next(step for step in leaves if step.rule is ProofRule.GIVEN)
    clone = replace(exactness)
    modified_trust = tuple(clone if step is exactness else step for step in trusted)
    with pytest.raises(ValueError, match="Untrusted GIVEN provenance root"):
        validate_phase161_r7_provenance(leaves, modified_trust)


def test_phase161_r7_rejects_cycle():
    leaves, _ = _fixture()
    witness = next(step for step in leaves if step.rule is ProofRule.INFERENCE)
    loop = replace(witness, premises=())
    object.__setattr__(loop, "premises", (loop,))
    with pytest.raises(ValueError, match="Cyclic proof ancestry"):
        validate_phase161_r7_provenance((loop,), ())
