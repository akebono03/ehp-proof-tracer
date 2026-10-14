"""Focused R23 non-certification and rule-reuse tests."""
from expression import Suspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_r23_existing_rule_adapter import _objects, expand_existing_pi43_rules
from proof import Relation


def test_r23_root_uses_existing_generator_rule():
    _, target, _, _, _, _, eta3, _ = _objects()
    expansions = expand_existing_pi43_rules(Relation(target, FiniteCyclicGroup(2, eta3)))
    assert len(expansions) == 1
    assert expansions[0].rule.name == "Toda pi_4^3 eta_3 generator notation"
    assert len(expansions[0].subgoals) == 2


def test_r23_quotient_uses_existing_rule():
    _, target, _, _, _, eta2, _, _ = _objects()
    expansions = expand_existing_pi43_rules(
        Relation(target, FiniteCyclicGroup(2, Suspension(expression=eta2)))
    )
    assert len(expansions) == 1
    assert expansions[0].rule.name == "Toda pi_4^3 finite cyclic quotient calculation"
    assert len(expansions[0].subgoals) == 3


def test_r23_kernel_and_surjectivity_remain_obligations():
    from phase165_r52_r23_existing_rule_adapter import _objects
    import toda_rules as rules
    from homotopy_groups import FreeCyclicGroup
    _, _, _, e, _, _, _, twice = _objects()
    kernel = rules.TodaSuspensionKernelFreeCyclicStatement(e, FreeCyclicGroup(twice))
    surjective = rules.TodaSuspensionSurjectiveStatement(e)
    assert len(expand_existing_pi43_rules(kernel)) == 1
    assert len(expand_existing_pi43_rules(surjective)) == 1


def test_r23_does_not_invent_delta_premise_or_other_targets():
    import toda_rules as rules
    from homotopy_groups import FreeCyclicGroup
    _, _, _, _, delta, _, _, twice = _objects()
    goal = rules.TodaDeltaImageFreeCyclicStatement(delta, FreeCyclicGroup(twice))
    assert expand_existing_pi43_rules(goal) == ()
    assert expand_existing_pi43_rules(Relation(TodaPrimaryGroup(7, 4), FiniteCyclicGroup(2, twice))) == ()
