"""Focused tests: candidate construction only, no synthetic proof certificates."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Multiple
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase169_r10d2_general_family_definition.family_citation import CitedStableFamilyDefinition
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    Toda55UniversalQuadrupleStatement, canonical_quadruple_goal,
)
from phase176_r3r40_toda55_connection_audit.source import (
    build_audit_connection_provider, quadruple_hopf_backward_plan,
)
from proof import Relation, RelationType


def example(n=5):
    forward = canonical_quadruple_goal(n)
    # The real R3R39 case has n=5; n=7 tests the structural generalization.
    sphere = (n + 1) // 2
    alpha = HomotopyElement("formal-alpha", sphere, n + 1, sphere)
    if n == 5:
        alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    cube = forward.rhs
    hopf = Relation(MapApplication(EHP_H_MAP, alpha), cube.left)
    goal = Relation(MapApplication(EHP_H_MAP, Composition(alpha, cube.right)), forward.lhs)
    sources = (Toda55UniversalQuadrupleStatement(), CitedStableFamilyDefinition(4, 4, 3),
               TodaEtaFamilyGeneralDefinition(), TodaProp22RightFormula(), hopf)
    return goal, forward, sources


@pytest.mark.parametrize("n", (5, 7))
def test_two_old_rules_and_exact_open_obligations(n):
    goal, forward, sources = example(n)
    plan = quadruple_hopf_backward_plan(goal, sources)
    reverse = Relation(forward.rhs, forward.lhs)
    transport = Relation(goal.lhs, forward.rhs)
    assert len(plan) == 2
    assert plan[0][0] == reverse
    assert plan[0][1].rule.name == "equality symmetry"
    assert plan[0][1].subgoals == (forward,)
    assert plan[1][0] == goal
    assert plan[1][1].rule.name == "equality transitivity"
    assert plan[1][1].subgoals == (transport, reverse)


def test_each_source_is_required_and_ambiguity_rejected():
    goal, _, sources = example()
    for i, source in enumerate(sources):
        assert quadruple_hopf_backward_plan(goal, sources[:i] + sources[i+1:]) == ()
        assert quadruple_hopf_backward_plan(goal, sources + (source,)) == ()
    with pytest.raises(TypeError):
        quadruple_hopf_backward_plan(goal, list(sources))


def test_rejects_wrong_coefficient_and_map_and_untyped_goal():
    goal, forward, sources = example()
    assert quadruple_hopf_backward_plan(replace(goal, rhs=Multiple(2, forward.lhs.expression)), sources) == ()
    assert quadruple_hopf_backward_plan(replace(goal, lhs=forward.rhs), sources) == ()
    assert quadruple_hopf_backward_plan(replace(goal, relation_type=RelationType.ZERO), sources) == ()
    assert quadruple_hopf_backward_plan("untyped", sources) == ()


def test_rejects_different_rhs_generator_and_right_factor():
    goal, forward, sources = example()
    wrong_nu = replace(forward.lhs.expression, name="different")
    assert quadruple_hopf_backward_plan(replace(goal, rhs=Multiple(4, wrong_nu)), sources) == ()
    product = goal.lhs.expression
    changed = Composition(product.right.left, replace(product.right.right, name="different"))
    wrong_goal = replace(goal, lhs=MapApplication(EHP_H_MAP, Composition(product.left, changed)))
    assert quadruple_hopf_backward_plan(wrong_goal, sources) == ()


def test_local_provider_does_not_claim_independent_inputs():
    goal, forward, sources = example()
    plan = quadruple_hopf_backward_plan(goal, sources)
    provider = build_audit_connection_provider(goal, sources)
    for target, expansion in plan:
        options = provider(target)
        assert len(options) == 1
        assert options[0].rule.name == expansion.rule.name
        assert options[0].subgoals == expansion.subgoals
    assert provider(forward) == ()
    assert provider(plan[1][1].subgoals[0]) == ()
    assert provider("unrelated") == ()
