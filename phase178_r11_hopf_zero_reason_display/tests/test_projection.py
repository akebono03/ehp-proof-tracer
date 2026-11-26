from dataclasses import replace

import pytest
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapSurjective
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import expand_e_surjective_from_delta_injective
from phase178_r11_hopf_zero_reason_display.projection import project_hopf_zero_reason
from phase168_r3_27_typed_statement_projection import typed_sentence
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


def fixture(n,q):
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(q,n),TodaPrimaryGroup(q+1,n+1)))
    option, = expand_e_surjective_from_delta_injective(goal)
    parents = tuple(ProofStep(g,(),ProofRule.INFERENCE) for g in option.subgoals)
    match, = find_inference_matches_for_rule(option.rule,parents)
    return goal,apply_inference_match(match)


@pytest.mark.parametrize('n,q',[(2,8),(3,8),(4,10)])
def test_reason(n,q):
    goal,step = fixture(n,q)
    expected = (rf"完全性より, $\operatorname{{Im}}H=\ker\Delta=0$ なので, "
                rf"$H$ は零写像. よって, $\operatorname{{Im}}E=\ker H=\pi_{{{q+1}}}^{{{n+1}}}$ となり, "
                rf"$E: \pi_{{{q}}}^{{{n}}}\to \pi_{{{q+1}}}^{{{n+1}}}$ は全射.")
    assert project_hopf_zero_reason(goal,step)==expected
    assert typed_sentence(goal,step)==expected


def test_reject_missing_wrong_and_unproved_parents():
    goal,step = fixture(2,8)
    other,other_step = fixture(3,8)
    a,b,c = step.premises
    for bad in (replace(step,premises=(a,b)),replace(step,premises=(a,c,b)),
                replace(step,premises=(other_step.premises[0],b,c)),
                replace(step,premises=(replace(a,rule=ProofRule.GIVEN),b,c)),
                replace(step,rule=ProofRule.GIVEN),replace(step,inference_rule=None)):
        assert project_hopf_zero_reason(goal,bad) is None
    assert project_hopf_zero_reason(other,step) is None
