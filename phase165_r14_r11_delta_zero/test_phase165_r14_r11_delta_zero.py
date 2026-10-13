from homotopy_groups import (
    TodaDeltaMap, TodaEHPExactnessWindow, TodaPrimaryGroup,
    TodaSuspensionIsomorphismStatement, TodaSuspensionMap,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from map_facts import EHP_E_MAP, EHP_DELTA_MAP
from toda_rules import TodaDeltaZeroStatement, TodaProp42ExactnessStatement
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r11_delta_zero import (
    audit_delta_pi32, delta_zero_from_suspension_iso_and_exactness_rule,
    expand_delta_zero_from_suspension_iso,
)


def _goal():
    return TodaDeltaZeroStatement(TodaDeltaMap(TodaPrimaryGroup(3,3), TodaPrimaryGroup(1,1)))


def _given(goal):
    return ProofStep(goal, (), ProofRule.GIVEN)


def test_delta_zero_requires_iso_and_exactness():
    expansions = expand_delta_zero_from_suspension_iso(_goal())
    assert len(expansions) == 1
    iso, ex = expansions[0].subgoals
    assert iso.map == TodaSuspensionMap(TodaPrimaryGroup(1,1), TodaPrimaryGroup(2,2))
    assert ex.window.first_map == EHP_DELTA_MAP
    assert ex.window.second_map == EHP_E_MAP


def test_matching_fixture_leaves_produce_derived_step():
    expansion = expand_delta_zero_from_suspension_iso(_goal())[0]
    matches = find_inference_matches_for_rule(
        expansion.rule, tuple(_given(x) for x in expansion.subgoals)
    )
    assert len(matches) == 1
    step = derive_inference_proof_step(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == _goal()


def test_wrong_suspension_iso_rejected():
    expansion = expand_delta_zero_from_suspension_iso(_goal())[0]
    other = TodaSuspensionIsomorphismStatement(
        TodaSuspensionMap(TodaPrimaryGroup(2,2),TodaPrimaryGroup(3,3))
    )
    matches = find_inference_matches_for_rule(expansion.rule, (
        _given(other), _given(expansion.subgoals[1]),
    ))
    assert matches == ()


def test_wrong_exactness_maps_rejected():
    expansion = expand_delta_zero_from_suspension_iso(_goal())[0]
    w = expansion.subgoals[1].window
    wrong = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        w.source_term, w.middle_term, w.target_term, EHP_E_MAP, EHP_DELTA_MAP,
    ))
    assert not find_inference_matches_for_rule(expansion.rule, (
        _given(expansion.subgoals[0]), _given(wrong),
    ))


def test_no_direct_proof_or_certification():
    report = audit_delta_pi32()
    assert report["expansions"] == 1
    assert report["toda_proof_steps_created"] == 0
    assert report["new_certified_leaves"] == 0


def test_unrelated_goal_has_no_expansion():
    assert expand_delta_zero_from_suspension_iso("delta=0") == ()
