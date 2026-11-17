"""Synthetic-premise contracts for the isolated *general* order-to-zero rule.

Test-created ProofSteps are NOT real published or independently verified proofs.
The audit authenticates the earlier pi_8^7 DB row without a proof replay.
"""
from __future__ import annotations

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, Multiple, Zero
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase175_r4r5_eta7_annihilator_isolated.rule import (
    RULE_NAME, expand_finite_cyclic_order_zero, finite_cyclic_order_zero_rule,
    order_zero_premise, typed_endpoints,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)


def eta(n: int) -> HomotopyElement:
    return HomotopyElement(
        name="η_" + str(n), dimension=n, source=n + 1, target=n,
        generator=GeneratorSymbol("η", index=n),
    )


def zero_goal(n: int, m: int = 2) -> Relation:
    return Relation(Multiple(m, eta(n)), Zero(), RelationType.EQUALITY)


def fake_proved_step(relation: Relation) -> ProofStep:
    """A shape-only test fixture: trust is separately checked by the audit."""
    return ProofStep(
        conclusion=relation, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="synthetic test-only prior"),
    )


def test_eta7_typed_order_two_premise() -> None:
    target = zero_goal(7)
    assert typed_endpoints(eta(7)) == (8, 7)
    assert order_zero_premise(target) == Relation(
        TodaPrimaryGroup(8, 7), FiniteCyclicGroup(2, eta(7)), RelationType.EQUALITY,
    )
    proposals = expand_finite_cyclic_order_zero(target)
    assert len(proposals) == 1
    assert proposals[0].subgoals == (order_zero_premise(target),)
    assert proposals[0].rule.name == RULE_NAME


@pytest.mark.parametrize("n,m", [(3, 2), (4, 3), (7, 2), (8, 4), (15, 8)])
def test_general_rule_works_outside_eta7(n: int, m: int) -> None:
    target = zero_goal(n, m)
    premise = order_zero_premise(target)
    assert premise is not None
    options = expand_finite_cyclic_order_zero(target)
    assert len(options) == 1
    matches = find_inference_matches_for_rule(
        options[0].rule, (fake_proved_step(premise),),
    )
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == target
    assert step.premises[0].conclusion == premise


def test_rule_rejects_unverified_relation_step_kind() -> None:
    goal = zero_goal(7)
    premise = order_zero_premise(goal)
    assert premise is not None
    fake_relation = ProofStep(premise, (), ProofRule.RELATION)
    rule = finite_cyclic_order_zero_rule(goal)
    assert find_inference_matches_for_rule(rule, (fake_relation,)) == ()
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert find_inference_matches_for_rule(rule, (fake_proved_step(
        Relation(TodaPrimaryGroup(8, 7), FiniteCyclicGroup(4, eta(7))),
    ),)) == ()


@pytest.mark.parametrize("bad", [
    Relation(Multiple(1, eta(7)), Zero()),
    Relation(Multiple(0, eta(7)), Zero()),
    Relation(Multiple(-2, eta(7)), Zero()),
    Relation(Multiple(2, eta(7)), eta(7)),
    Relation(Multiple(2, eta(7)), Zero(), RelationType.ORDER),
    Relation(eta(7), Zero()),
    Relation(Multiple(2, eta(7)), Zero(), source="fabricated citation"),
    Relation(Multiple(2, eta(7)), Zero(), note="unreviewed"),
    Relation(Multiple(True, eta(7)), Zero()),
])
def test_invalid_goal_never_generates_rule(bad: Relation) -> None:
    assert expand_finite_cyclic_order_zero(bad) == ()
    assert order_zero_premise(bad) is None
    with pytest.raises(ValueError, match="typed finite-order"):
        finite_cyclic_order_zero_rule(bad)


def test_sphere_dimension_mismatch_fails_closed() -> None:
    bogus = HomotopyElement(
        "η_7", dimension=8, source=8, target=7,
        generator=GeneratorSymbol("η", index=7),
    )
    assert typed_endpoints(bogus) is None
    assert expand_finite_cyclic_order_zero(Relation(Multiple(2, bogus), Zero())) == ()
    incomplete = HomotopyElement("g", dimension=7, source=None, target=7)
    assert typed_endpoints(incomplete) is None


def test_composition_endpoint_guard() -> None:
    first = HomotopyElement("f", dimension=4, source=7, target=4)
    second = HomotopyElement("g", dimension=7, source=8, target=7)
    comp = Composition(first, second)
    assert typed_endpoints(comp) == (8, 4)
    assert order_zero_premise(Relation(Multiple(2, comp), Zero())) == Relation(
        TodaPrimaryGroup(8, 4), FiniteCyclicGroup(2, comp),
    )
    malformed = Composition(second, first)
    assert typed_endpoints(malformed) is None


def test_source_only_is_never_sufficient_for_verified_parent() -> None:
    goal = zero_goal(7)
    options = expand_finite_cyclic_order_zero(goal)
    assert options[0].subgoals == (order_zero_premise(goal),)
    assert len(options) == 1
    assert options[0].rule.premise_patterns[0].proof_rule is None


def test_each_direct_sum_generator_independently_annihilated() -> None:
    from homotopy_groups import DirectSumGroup, FreeCyclicGroup

    a = HomotopyElement("a", 4, source=8, target=4)
    b = HomotopyElement("b", 4, source=8, target=4)
    c = HomotopyElement("c", 4, source=8, target=4)
    group = TodaPrimaryGroup(8, 4)
    presentation = Relation(
        group,
        DirectSumGroup((FreeCyclicGroup(c), FiniteCyclicGroup(2, a),
                        FiniteCyclicGroup(4, b))),
    )
    for m, gen in ((2, a), (4, b)):
        goal = Relation(Multiple(m, gen), Zero())
        assert order_zero_premise(goal, presentation) == presentation
        proposals = expand_finite_cyclic_order_zero(goal, (presentation,))
        assert len(proposals) == 1
        assert proposals[0].subgoals == (presentation,)
        matches = find_inference_matches_for_rule(
            proposals[0].rule, (fake_proved_step(presentation),),
        )
        assert len(matches) == 1
        step = apply_inference_match(matches[0])
        assert step.conclusion == goal
        assert step.premises[0].conclusion == presentation
    assert order_zero_premise(Relation(Multiple(2, c), Zero()), presentation) is None
    assert expand_finite_cyclic_order_zero(
        Relation(Multiple(2, c), Zero()), (presentation,),
    ) == ()


def test_nested_direct_sum_and_duplicate_candidates() -> None:
    from homotopy_groups import DirectSumGroup, FreeCyclicGroup
    a = HomotopyElement("a", 5, source=9, target=5)
    b = HomotopyElement("b", 5, source=9, target=5)
    presentation = Relation(TodaPrimaryGroup(9, 5), DirectSumGroup((
        FreeCyclicGroup(a), DirectSumGroup((FiniteCyclicGroup(8, b),)),
    )))
    goal = Relation(Multiple(8, b), Zero())
    assert order_zero_premise(goal, presentation) == presentation
    options = expand_finite_cyclic_order_zero(goal, (presentation, presentation))
    assert len(options) == 1
    assert options[0].subgoals == (presentation,)


@pytest.mark.parametrize("invalid", [
    "wrong_order", "wrong_generator", "wrong_group", "not_in_direct_sum",
    "wrong_relation", "zero_order", "trivial_order",
])
def test_direct_sum_source_fail_closed(invalid: str) -> None:
    from homotopy_groups import DirectSumGroup, FreeCyclicGroup
    a = HomotopyElement("a", 4, source=8, target=4)
    b = HomotopyElement("b", 4, source=8, target=4)
    goal = Relation(Multiple(2, a), Zero())
    if invalid == "wrong_order":
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(4, a),)))
    elif invalid == "wrong_generator":
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(2, b),)))
    elif invalid == "wrong_group":
        source = Relation(TodaPrimaryGroup(9, 4), DirectSumGroup((FiniteCyclicGroup(2, a),)))
    elif invalid == "not_in_direct_sum":
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FreeCyclicGroup(a),)))
    elif invalid == "wrong_relation":
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(2, a),)), RelationType.ORDER)
    elif invalid == "zero_order":
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(0, a),)))
    else:
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(1, a),)))
    assert order_zero_premise(goal, source) is None
    assert expand_finite_cyclic_order_zero(goal, (source,)) == ()
    with pytest.raises(ValueError, match="finite-cyclic summand"):
        finite_cyclic_order_zero_rule(goal, source)


def test_source_first_candidates_are_not_self_certifying() -> None:
    from homotopy_groups import DirectSumGroup
    a = HomotopyElement("a", 4, source=8, target=4)
    presentation = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(2, a),)))
    goal = Relation(Multiple(2, a), Zero())
    proposals = expand_finite_cyclic_order_zero(goal, (presentation,))
    assert len(proposals) == 1
    assert proposals[0].subgoals == (presentation,)
    assert find_inference_matches_for_rule(proposals[0].rule, ()) == ()
    unproved_relation = ProofStep(presentation, (), ProofRule.RELATION)
    assert find_inference_matches_for_rule(proposals[0].rule, (unproved_relation,)) == ()
    incorrect_step = fake_proved_step(Relation(
        TodaPrimaryGroup(8, 4), FiniteCyclicGroup(2, a),
    ))
    assert find_inference_matches_for_rule(proposals[0].rule, (incorrect_step,)) == ()
    with pytest.raises(TypeError, match="tuple"):
        expand_finite_cyclic_order_zero(goal, [presentation])


def test_iterated_suspension_and_composition_endpoints_for_real_shape() -> None:
    from expression import IteratedSuspension, Suspension, Sum
    nu_prime = HomotopyElement("nu-prime", 3, source=6, target=3)
    eta7 = HomotopyElement("eta7", 7, source=8, target=7)
    first = IteratedSuspension(nu_prime, 1)
    assert typed_endpoints(first) == (7, 4)
    assert typed_endpoints(Suspension(nu_prime)) == (7, 4)
    assert typed_endpoints(Composition(first, eta7)) == (8, 4)
    assert typed_endpoints(IteratedSuspension(nu_prime, -1)) is None
    assert typed_endpoints(IteratedSuspension(nu_prime, True)) is None
    assert typed_endpoints(Sum(first, first)) == (7, 4)
    assert typed_endpoints(Sum(first, eta7)) is None
    assert typed_endpoints(Multiple(2, first)) == (7, 4)


def test_direct_sum_candidate_requires_exact_ambient_endpoints() -> None:
    from homotopy_groups import DirectSumGroup
    gen = HomotopyElement("g", 4, source=8, target=4)
    another = HomotopyElement("g", 5, source=9, target=5)
    source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(2, gen),)))
    assert order_zero_premise(Relation(Multiple(2, another), Zero()), source) is None
    assert order_zero_premise(Relation(Multiple(4, gen), Zero()), source) is None
    assert order_zero_premise(Relation(Multiple(2, gen), Zero()), source) == source


def test_zero_relation_type_is_supported_as_a_general_zero_goal() -> None:
    from homotopy_groups import DirectSumGroup
    a = HomotopyElement("a", 4, source=8, target=4)
    presentation = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(2, a),)))
    goal = Relation(Multiple(2, a), Zero(), RelationType.ZERO)
    proposals = expand_finite_cyclic_order_zero(goal, (presentation,))
    assert len(proposals) == 1
    matches = find_inference_matches_for_rule(
        proposals[0].rule, (fake_proved_step(presentation),),
    )
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == goal
