from dataclasses import replace

import pytest

from phase162_r2_existing_proof_connection import (
    reconstruct_phase162_r2_from_existing_proofs,
)
from proof import ProofRule, ProofStep
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from tests.test_phase59_toda52_pi4_2_transport import build_phase59_2_data
from tests.test_phase59_pi5_3_eta3_squared import build_phase59_4_data


def _inputs():
    group = build_phase59_2_data()
    target = build_phase59_4_data()
    ehp = build_phase59_3_data()
    source = group["result_steps"][0]
    definitions = (
        target["eta3_definition_step"],
        target["eta4_definition_step"],
    )
    roots = {}

    def visit(step):
        if step.rule is ProofRule.GIVEN:
            roots[id(step)] = step
            return
        for premise in step.premises:
            visit(premise)

    for step in (source,) + definitions + ehp["premise_steps"]:
        visit(step)
    return (
        target["expected_pi5_3_relation"],
        ehp["expected_suspension_isomorphism"].map,
        (source,),
        definitions,
        ehp["premise_steps"],
        tuple(roots.values()),
    )


def test_phase162_r2_connects_derived_source_and_bridge():
    args = _inputs()
    result = reconstruct_phase162_r2_from_existing_proofs(*args)
    assert result.reconstruction.final_step.conclusion == args[0]
    assert len(result.reconstruction.derived_steps) == 8
    assert result.source_structure_step is args[2][0]
    assert result.source_structure_step.rule is ProofRule.INFERENCE
    assert result.generator_image_step.rule is ProofRule.INFERENCE
    assert result.generator_image_step.premises == args[3]
    assert result.reconstruction.final_step.premises[1] is result.source_structure_step
    assert result.reconstruction.final_step.premises[2] is result.generator_image_step
    assert result.provenance.verified_inferences >= 9


def test_phase162_r2_rejects_missing_source_proof():
    args = list(_inputs())
    args[2] = ()
    with pytest.raises(ValueError, match="derived source-group"):
        reconstruct_phase162_r2_from_existing_proofs(*args)


def test_phase162_r2_rejects_given_source_instead_of_derived():
    args = list(_inputs())
    args[2] = (replace(args[2][0], rule=ProofRule.GIVEN, premises=(), inference_rule=None),)
    with pytest.raises(ValueError, match="derived source-group"):
        reconstruct_phase162_r2_from_existing_proofs(*args)


def test_phase162_r2_rejects_missing_eta_definition():
    args = list(_inputs())
    args[3] = args[3][:1]
    with pytest.raises(ValueError, match="eta-family definition bridge"):
        reconstruct_phase162_r2_from_existing_proofs(*args)


def test_phase162_r2_rejects_untrusted_provenance():
    args = list(_inputs())
    args[5] = ()
    with pytest.raises(ValueError, match="Untrusted GIVEN provenance root"):
        reconstruct_phase162_r2_from_existing_proofs(*args)
