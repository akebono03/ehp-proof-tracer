from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_12_body_binding import build_narrative_body_lines
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep


def _case():
    rule = InferenceRule(name="source", literature_reference=LiteratureReference(label="Toda (5.2)", locator="(5.2)"))
    step = ProofStep(conclusion="root", premises=(), rule=ProofRule.INFERENCE, inference_rule=rule)
    result = make_partial_proof_result(n=2, k=2, status=ProofSearchStatus.COMPLETE,
                                       proven_steps=(step,), conclusion="root")
    return result, build_proof_narrative_model(result)


def test_citation_numbers_are_bound_to_actual_steps():
    result, model = _case()
    assert model.step_citation_numbers == ((1,),)
    assert model.citations[0].step_indices == (0,)
    assert build_narrative_body_lines(result, model) == ()  # no fabricated repr for root


def test_unknown_citation_number_is_rejected():
    result, model = _case()
    wrong = replace(model, step_citation_numbers=((2,),))
    with pytest.raises(ValueError, match="citation and step map disagree"):
        build_narrative_body_lines(result, wrong)


def test_reverse_citation_mapping_is_checked():
    result, model = _case()
    wrong = replace(model, step_citation_numbers=((),))
    with pytest.raises(ValueError, match="disagree"):
        build_narrative_body_lines(result, wrong)


def test_mismatched_search_result_is_rejected():
    result, model = _case()
    other = replace(result, proven_steps=(ProofStep(conclusion="root", premises=(), rule=ProofRule.GIVEN),))
    with pytest.raises(ValueError, match="must match"):
        build_narrative_body_lines(other, model)
