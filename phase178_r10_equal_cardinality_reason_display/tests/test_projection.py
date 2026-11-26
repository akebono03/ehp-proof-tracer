"""Test the direct reason, its guards and the shared formatter hook."""
from dataclasses import replace

import pytest

from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase168_r3_27_typed_statement_projection import map_property_sentence, typed_sentence
from phase178_r8_finite_group_surjective_injective_isolated.rule import expand_finite_surjective_injective
from phase178_r10_equal_cardinality_reason_display.projection import project_equal_cardinality_reason
from proof import InferenceRule, ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


def make_step(mapping, order):
    goal = MapInjective(mapping)
    option, = expand_finite_surjective_injective(goal, order)
    parents = tuple(ProofStep(x, (), ProofRule.INFERENCE, inference_rule=InferenceRule('test-only hypothesis')) for x in option.subgoals)
    match, = [m for m in find_inference_matches_for_rule(option.rule, parents) if m.premises == parents]
    return apply_inference_match(match)


@pytest.mark.parametrize('mapping,order,symbol', [
    (TodaDeltaMap(TodaPrimaryGroup(9,5),TodaPrimaryGroup(7,2)),2,r'\Delta'),
    (TodaDeltaMap(TodaPrimaryGroup(12,9),TodaPrimaryGroup(10,4)),8,r'\Delta'),
    (TodaSuspensionMap(TodaPrimaryGroup(8,4),TodaPrimaryGroup(9,5)),4,'E'),
    (TodaHopfInvariantMap(TodaPrimaryGroup(10,4),TodaPrimaryGroup(10,7)),8,'H'),
])
def test_generic_reason(mapping, order, symbol):
    step = make_step(mapping,order)
    a,b = mapping.source_group,mapping.target_group
    source = rf'\pi_{{{a.group_dimension}}}^{{{a.sphere_dimension}}}'
    target = rf'\pi_{{{b.group_dimension}}}^{{{b.sphere_dimension}}}'
    expected = (rf'$|{source}|=|{target}|={order}$ であり, ${symbol}$ は全射なので, '
                rf'${symbol}: {source}\to {target}$ は単射.')
    assert project_equal_cardinality_reason(step.conclusion,step)==expected
    assert map_property_sentence(step.conclusion,step)==expected
    assert typed_sentence(step.conclusion,step)==expected


def test_malformed_premises_are_not_explained_as_equal_cardinality():
    step = make_step(TodaDeltaMap(TodaPrimaryGroup(9,5),TodaPrimaryGroup(7,2)),2)
    a,b,surj=step.premises
    for parents in ((a,b),(replace(a,conclusion=replace(a.conclusion,order=4)),b,surj),
                    (a,replace(b,rule=ProofRule.GIVEN),surj),
                    (a,b,replace(surj,conclusion=replace(surj.conclusion,map=TodaDeltaMap(TodaPrimaryGroup(10,5),TodaPrimaryGroup(8,2)))))):
        bad=replace(step,premises=parents)
        assert project_equal_cardinality_reason(step.conclusion,bad) is None
        plain=map_property_sentence(step.conclusion,bad)
        assert plain == r'$\Delta: \pi_{9}^{5}\to \pi_{7}^{2}$ は単射.'
    assert project_equal_cardinality_reason(step.conclusion,replace(step,rule=ProofRule.GIVEN)) is None
    assert project_equal_cardinality_reason(step.conclusion,replace(step,inference_rule=InferenceRule('other'))) is None
