"""Focused cyclic-structure source, type, rule and public-path regressions."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
from phase171_r2j_r4_r9_r9_public_cyclic_structure.source import (
    expand_cited_full_order_cyclic_structure,
    finite_cyclic_structure_from_full_order_rule,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _case():
    nu = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    db_nu = HomotopyElement(
        name="ν'", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family=r"\nu'"),
    )
    group = TodaPrimaryGroup(6, 3)
    source = Relation(Multiple(2, nu), "typed cited RHS", RelationType.EQUALITY)
    goal = CyclicStructureStatement(group, db_nu, 4)
    return source, goal, nu


def test_source_anchored_structure_is_only_two_unproved_subgoals():
    source, goal, nu = _case()
    routes = expand_cited_full_order_cyclic_structure(goal, (source,))
    assert len(routes) == 1
    assert routes[0].subgoals == (
        FiniteGroupCardinality(goal.group, 4),
        FiniteElementOrder(goal.group, nu, 4),
    )
    assert not any(isinstance(item, ProofStep) for item in routes[0].subgoals)


def test_matched_order_and_group_derive_one_real_cyclic_structure():
    source, goal, _ = _case()
    route, = expand_cited_full_order_cyclic_structure(goal, (source,))
    parents = tuple(ProofStep(value, (), ProofRule.INFERENCE) for value in route.subgoals)
    matches = find_inference_matches_for_rule(route.rule, parents)
    assert len(matches) == 1
    result = derive_inference_proof_step(matches[0])
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert result.premises == parents


def test_givens_cannot_replace_proved_orders():
    source, goal, _ = _case()
    route, = expand_cited_full_order_cyclic_structure(goal, (source,))
    left, right = route.subgoals
    rule = finite_cyclic_structure_from_full_order_rule(goal)
    for parents in (
        (ProofStep(left, (), ProofRule.GIVEN), ProofStep(right, (), ProofRule.INFERENCE)),
        (ProofStep(left, (), ProofRule.INFERENCE), ProofStep(right, (), ProofRule.GIVEN)),
    ):
        assert find_inference_matches_for_rule(rule, parents) == ()


def test_missing_screened_source_or_bad_generator_fails_closed():
    source, goal, nu = _case()
    assert expand_cited_full_order_cyclic_structure(goal, ()) == ()
    bad = replace(nu, generator=GeneratorSymbol(family="σ", index=3))
    assert expand_cited_full_order_cyclic_structure(
        goal, (replace(source, lhs=Multiple(2, bad)),),
    ) == ()


def test_cited_relation_must_be_typed_and_double():
    source, goal, nu = _case()
    assert expand_cited_full_order_cyclic_structure(
        goal, (replace(source, relation_type=RelationType.INEQUALITY),),
    ) == ()
    assert expand_cited_full_order_cyclic_structure(
        goal, (replace(source, lhs=Multiple(3, nu)),),
    ) == ()
    assert expand_cited_full_order_cyclic_structure(
        goal, (replace(source, lhs=Multiple(2, replace(nu, source=7))),),
    ) == ()


def test_invalid_goal_and_bad_container_are_rejected():
    source, goal, _ = _case()
    with pytest.raises(TypeError):
        expand_cited_full_order_cyclic_structure(goal, [source])
    assert expand_cited_full_order_cyclic_structure("invalid", (source,)) == ()
    with pytest.raises(ValueError):
        finite_cyclic_structure_from_full_order_rule(
            replace(goal, order=0),
        )


def test_other_cardinality_does_not_become_asserted_order():
    source, goal, _ = _case()
    # R7 currently provides only source-anchored order-four proposals.
    assert expand_cited_full_order_cyclic_structure(
        replace(goal, order=8), (source,),
    ) == ()
    assert expand_cited_full_order_cyclic_structure(
        replace(goal, order=2), (source,),
    ) == ()


def test_duplicate_source_does_not_duplicate_proposals():
    source, goal, _ = _case()
    assert len(expand_cited_full_order_cyclic_structure(goal, (source, source))) == 1


def test_public_provider_matches_existing_r4_r8_verified_parents():
    from phase171_r2j_r4_r9_r9_public_cyclic_structure.audit import (
        inspect_public_cyclic_structure,
    )
    report = inspect_public_cyclic_structure()
    assert report["shared_structure_connected"] is True
    assert report["structure_inference_matched"] is True
    assert report["new_given_added"] == 0
    assert report["completed_proof_imported"] is False


def test_prior_scoped_search_and_trust_boundary_remain_complete():
    from phase171_r2j_r4_r9_r6_source_bound_cited_hopf.audit import (
        audit_second_source_bound_hopf,
    )
    report = audit_second_source_bound_hopf()
    assert report["scoped_search_complete"] is True
    assert report["trust_boundary_accepted"] is True
    assert report["new_given_added"] == 0
