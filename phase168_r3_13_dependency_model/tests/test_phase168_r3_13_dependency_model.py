from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_13_dependency_model import build_narrative_inferences
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep


def _case():
    source = ProofStep("A", (), ProofRule.GIVEN)
    rule = InferenceRule(name="derived", literature_reference=LiteratureReference(
        label="Toda (5.2)", locator="(5.2)"
    ))
    derived = ProofStep("B", ("A",), ProofRule.INFERENCE, inference_rule=rule)
    result = make_partial_proof_result(
        n=2, k=2, status=ProofSearchStatus.COMPLETE,
        proven_steps=(source, derived), conclusion="B",
    )
    return result, build_proof_narrative_model(result)


def test_exact_prior_premise_dependency_and_source():
    result, model = _case()
    nodes = build_narrative_inferences(result, model)
    assert nodes[1].premise_indices == (0,)
    assert nodes[1].unresolved_premises == ()
    assert nodes[1].citation_numbers == (1,)
    assert nodes[1].is_root


def test_unresolved_premise_is_not_invented():
    result, model = _case()
    wrong = replace(result.proven_steps[1], premises=("UNKNOWN",))
    changed = replace(result, proven_steps=(result.proven_steps[0], wrong))
    changed_model = build_proof_narrative_model(changed)
    nodes = build_narrative_inferences(changed, changed_model)
    assert nodes[1].premise_indices == ()
    assert nodes[1].unresolved_premises == ("UNKNOWN",)


def test_forward_dependency_is_not_accepted():
    result, model = _case()
    first = replace(result.proven_steps[0], premises=("B",))
    changed = replace(result, proven_steps=(first, result.proven_steps[1]))
    nodes = build_narrative_inferences(changed, build_proof_narrative_model(changed))
    assert nodes[0].unresolved_premises == ("B",)


def test_mismatch_rejected():
    result, model = _case()
    other = replace(result, proven_steps=tuple(reversed(result.proven_steps)))
    with pytest.raises(ValueError, match="must match"):
        build_narrative_inferences(other, model)
