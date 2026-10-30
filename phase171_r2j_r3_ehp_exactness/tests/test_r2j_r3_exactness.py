"""Proven H-surjectivity and cited exactness must justify Delta=0 and E injective."""
from __future__ import annotations

from homotopy_groups import (
    TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase171_r2j_r3_ehp_exactness.audit import _goals, build_r2j_r3_proof
from phase171_r2j_r3_ehp_exactness.source import (
    _delta_e_inputs, _h_delta_inputs, delta_zero_from_surjective_hopf_rule,
    expand_cited_ehp_surjectivity_consequences,
    suspension_injective_from_zero_delta_rule,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from toda_rules import TodaDeltaZeroStatement


def test_full_proof_replays_h_and_both_exactness_windows():
    delta_root, injective_root, nodes, reference = build_r2j_r3_proof()
    assert delta_root.rule is ProofRule.INFERENCE
    assert injective_root.rule is ProofRule.INFERENCE
    assert injective_root.premises[0].conclusion == delta_root.conclusion
    assert sum(node.rule is ProofRule.GIVEN for node in nodes) == 5
    assert sum(node.rule is ProofRule.INFERENCE for node in nodes) >= 18
    assert reference.step.rule is ProofRule.GIVEN


def test_consecutive_ehp_windows_are_well_typed():
    delta, injective = _goals()
    hopf_surj, h_delta = _h_delta_inputs(delta)
    zero, delta_e = _delta_e_inputs(injective)
    assert zero == delta
    assert hopf_surj == MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))
    assert prop42_exactness_indices(h_delta) == (2, 7, "h_delta")
    assert prop42_exactness_indices(delta_e) == (2, 6, "delta_e")
    assert len(expand_cited_ehp_surjectivity_consequences(delta)) == 1
    assert len(expand_cited_ehp_surjectivity_consequences(injective)) == 1


def test_forged_given_surjectivity_and_exactness_are_rejected():
    delta, _ = _goals()
    surj, exact = _h_delta_inputs(delta)
    rule = delta_zero_from_surjective_hopf_rule(delta)
    forged = (ProofStep(surj, (), ProofRule.GIVEN), ProofStep(exact, (), ProofRule.GIVEN))
    assert find_inference_matches_for_rule(rule, forged) == ()
    assert find_inference_matches_for_rule(rule, (
        ProofStep(surj, (), ProofRule.INFERENCE), forged[1],
    )) == ()


def test_forged_given_delta_and_exactness_are_rejected():
    delta, injective = _goals()
    zero, exact = _delta_e_inputs(injective)
    assert delta == zero
    rule = suspension_injective_from_zero_delta_rule(injective)
    forged = (ProofStep(zero, (), ProofRule.GIVEN), ProofStep(exact, (), ProofRule.GIVEN))
    assert find_inference_matches_for_rule(rule, forged) == ()
    assert find_inference_matches_for_rule(rule, (
        ProofStep(zero, (), ProofRule.INFERENCE), forged[1],
    )) == ()


def test_wrong_delta_and_suspension_indices_fail_closed():
    delta, injective = _goals()
    invalid = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 5), TodaPrimaryGroup(6, 2),
    ))
    assert _h_delta_inputs(invalid) is None
    assert expand_cited_ehp_surjectivity_consequences(invalid) == ()
    wrong = MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
    ))
    assert _delta_e_inputs(wrong) is None
    assert expand_cited_ehp_surjectivity_consequences(wrong) == ()
    assert _h_delta_inputs(delta) is not None
    assert _delta_e_inputs(injective) is not None


def test_unrelated_exactness_window_cannot_substitute():
    delta, _ = _goals()
    surj, exact = _h_delta_inputs(delta)
    other = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(8, 5), TodaPrimaryGroup(6, 2),
    ))
    _, other_exact = _h_delta_inputs(other)
    rule = delta_zero_from_surjective_hopf_rule(delta)
    premises = (
        ProofStep(surj, (), ProofRule.INFERENCE),
        ProofStep(other_exact, (), ProofRule.INFERENCE),
    )
    assert find_inference_matches_for_rule(rule, premises) == ()
    assert exact != other_exact
