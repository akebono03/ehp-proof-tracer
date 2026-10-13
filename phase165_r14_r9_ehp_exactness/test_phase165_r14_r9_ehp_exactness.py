from homotopy_groups import (
    TodaPrimaryGroup, TodaHopfInvariantMap, TodaPrimaryGroupZeroStatement
)
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r14_r9_ehp_exactness import (
    expand_generic_ehp_hopf_goal,
    hopf_injective_from_exactness_rule,
    hopf_surjective_from_exactness_rule,
    audit_pi32_hopf_exactness,
)
from proof import ProofStep, ProofRule, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step


def _h(n=2, q=3):
    return TodaHopfInvariantMap(
        TodaPrimaryGroup(q, n), TodaPrimaryGroup(q, 2*n-1)
    )


def _given(content):
    return ProofStep(content, (), ProofRule.GIVEN)


def test_hopf_injectivity_obligations():
    e = expand_generic_ehp_hopf_goal(MapInjective(_h()))
    assert len(e) == 1
    assert e[0].subgoals[0] == TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(2,1))
    assert len(e[0].subgoals) == 2


def test_hopf_surjectivity_obligations():
    e = expand_generic_ehp_hopf_goal(MapSurjective(_h()))
    assert len(e) == 1
    assert len(e[0].subgoals) == 2
    assert e[0].subgoals[0].map.source_group == TodaPrimaryGroup(3,3)


def test_injective_rule_applies_to_matching_fixture_evidence():
    e = expand_generic_ehp_hopf_goal(MapInjective(_h()))[0]
    matches = find_inference_matches_for_rule(e.rule, tuple(map(_given,e.subgoals)))
    assert len(matches) == 1
    assert derive_inference_proof_step(matches[0]).conclusion == MapInjective(_h())


def test_surjective_rule_applies_to_matching_fixture_evidence():
    e = expand_generic_ehp_hopf_goal(MapSurjective(_h()))[0]
    matches = find_inference_matches_for_rule(e.rule, tuple(map(_given,e.subgoals)))
    assert len(matches) == 1
    assert derive_inference_proof_step(matches[0]).conclusion == MapSurjective(_h())


def test_wrong_exactness_window_is_rejected():
    e = expand_generic_ehp_hopf_goal(MapInjective(_h()))[0]
    unrelated = expand_generic_ehp_hopf_goal(MapInjective(_h(3,5)))[0]
    mismatched = (_given(e.subgoals[0]), _given(unrelated.subgoals[1]))
    assert not find_inference_matches_for_rule(hopf_injective_from_exactness_rule(), mismatched)


def test_wrong_delta_is_rejected():
    e = expand_generic_ehp_hopf_goal(MapSurjective(_h()))[0]
    unrelated = expand_generic_ehp_hopf_goal(MapSurjective(_h(3,5)))[0]
    mismatched = (_given(e.subgoals[0]), _given(unrelated.subgoals[1]))
    assert not find_inference_matches_for_rule(hopf_surjective_from_exactness_rule(), mismatched)


def test_invalid_degree_rejected():
    other = TodaHopfInvariantMap(TodaPrimaryGroup(3,2), TodaPrimaryGroup(3,4))
    assert expand_generic_ehp_hopf_goal(MapInjective(other)) == ()
    assert expand_generic_ehp_hopf_goal(MapSurjective(other)) == ()


def test_audit_retains_unverified_status():
    report = audit_pi32_hopf_exactness()
    assert report["injectivity_expansions"] == 1
    assert report["surjectivity_expansions"] == 1
    assert report["proof_steps_created_for_toda"] == 0
    assert report["source_certified"] is False
