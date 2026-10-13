from dataclasses import replace
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r16_foundational_suspension import (
    FOUNDATIONAL_SUSPENSION_IDENTITY,
    instantiate_foundational_identity_suspension,
)
from phase165_r14_r17_foundational_proofstep import (
    derive_foundational_suspension_step, audit_r17,
)
from proof import ProofRule


def test_foundational_step_has_explicit_provenance():
    claim = instantiate_foundational_identity_suspension(1)
    step = derive_foundational_suspension_step(claim.statement)
    assert step is not None
    assert step.conclusion == claim.statement
    assert step.rule is ProofRule.GIVEN
    assert step.foundational_reference == FOUNDATIONAL_SUSPENSION_IDENTITY
    assert step.premises == ()


def test_applies_to_arbitrary_diagonal_dimension():
    for n in (1, 2, 3, 8):
        goal = instantiate_foundational_identity_suspension(n).statement
        assert derive_foundational_suspension_step(goal).conclusion == goal


def test_rejects_wrong_generator_correspondence():
    valid = instantiate_foundational_identity_suspension(2).statement
    wrong = replace(valid, target_generator=valid.source_generator)
    assert derive_foundational_suspension_step(wrong) is None


def test_rejects_wrong_target_group():
    valid = instantiate_foundational_identity_suspension(2).statement
    wrong_map = TodaSuspensionMap(TodaPrimaryGroup(2,2), TodaPrimaryGroup(4,4))
    assert derive_foundational_suspension_step(replace(valid, map=wrong_map)) is None


def test_rejects_non_statement():
    assert derive_foundational_suspension_step("E iota_n = iota_n+1") is None


def test_audit_does_not_claim_toda_approval():
    report = audit_r17()
    assert report["foundational_identity_step_created"] == 1
    assert report["registered_proof_eligible_added"] == 0
    assert report["proposition42_application_approved"] is False
    assert report["pi32_proved"] is False
