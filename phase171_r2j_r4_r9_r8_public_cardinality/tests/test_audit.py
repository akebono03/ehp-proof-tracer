"""Focused regression tests for screened finite-cardinality backward goals."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2j_r4_r5_short_exact_sequence.source import EHPShortExactSequence
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r9_r8_public_cardinality.source import (
    _cited_finite_group_candidates,
    expand_cited_ehp_middle_cardinality,
)
from proof import ProofStep, Relation, RelationType


def _case():
    a = TodaPrimaryGroup(5, 2)
    b = TodaPrimaryGroup(6, 3)
    c = TodaPrimaryGroup(6, 5)
    left = Relation(
        a,
        FiniteCyclicGroup(2, HomotopyElement(
            name="left", dimension=2, source=5, target=2,
            generator=GeneratorSymbol(family="η", index=2),
        )),
        RelationType.EQUALITY,
    )
    right = Relation(
        c,
        FiniteCyclicGroup(2, HomotopyElement(
            name="right", dimension=5, source=6, target=5,
            generator=GeneratorSymbol(family="η", index=5),
        )),
        RelationType.EQUALITY,
    )
    return FiniteGroupCardinality(b, 4), left, right


def test_end_groups_yield_only_one_typed_backward_obligation():
    goal, left, right = _case()
    proposals = expand_cited_ehp_middle_cardinality(goal, (left, right))
    assert len(proposals) == 1
    option = proposals[0]
    assert isinstance(option, GoalExpansion)
    assert option.rule.name == "finite middle-group cardinality from short exact sequence"
    assert option.subgoals[0] == left
    assert isinstance(option.subgoals[1], EHPShortExactSequence)
    assert option.subgoals[2] == right
    assert not any(isinstance(item, ProofStep) for item in option.subgoals)


def test_missing_or_wrong_group_source_fails_closed():
    goal, left, right = _case()
    assert expand_cited_ehp_middle_cardinality(goal, (left,)) == ()
    assert expand_cited_ehp_middle_cardinality(goal, (right,)) == ()
    wrong = replace(left, lhs=TodaPrimaryGroup(5, 3))
    assert expand_cited_ehp_middle_cardinality(goal, (wrong, right)) == ()


def test_product_order_must_be_proved_not_assumed():
    goal, left, right = _case()
    assert expand_cited_ehp_middle_cardinality(replace(goal, order=8), (left, right)) == ()
    wrong = replace(right, rhs=FiniteCyclicGroup(3, right.rhs.generator))
    assert expand_cited_ehp_middle_cardinality(goal, (left, wrong)) == ()


def test_ambiguous_end_group_presentations_fail_closed():
    goal, left, right = _case()
    ambiguous = replace(right, rhs=FiniteCyclicGroup(
        2, replace(right.rhs.generator, name="different"),
    ))
    assert expand_cited_ehp_middle_cardinality(goal, (left, right, ambiguous)) == ()


def test_duplicate_exact_sources_are_deduplicated():
    goal, left, right = _case()
    assert len(expand_cited_ehp_middle_cardinality(goal, (left, left, right, right))) == 1
    assert _cited_finite_group_candidates(left.lhs, (left, left)) == (left,)


def test_non_ehp_dimensions_and_bad_input_are_rejected():
    goal, left, right = _case()
    with pytest.raises(TypeError):
        expand_cited_ehp_middle_cardinality(goal, [left, right])
    assert expand_cited_ehp_middle_cardinality("not a cardinality", (left, right)) == ()
    assert expand_cited_ehp_middle_cardinality(
        FiniteGroupCardinality(TodaPrimaryGroup(6, 4), 4), (left, right),
    ) == ()
    assert expand_cited_ehp_middle_cardinality(
        FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 0), (left, right),
    ) == ()


def test_public_provider_matches_actual_verified_r4_r6_cardinality():
    from phase171_r2j_r4_r9_r8_public_cardinality.audit import inspect_public_cardinality
    report = inspect_public_cardinality()
    assert report["shared_cardinality_connected"] is True
    assert report["source_anchored_cardinality_routes"] == 1
    assert report["new_given_added"] == 0
    assert report["completed_proof_imported"] is False


def test_scoped_canonical_search_is_still_complete_and_trusted():
    from phase171_r2j_r4_r9_r6_source_bound_cited_hopf.audit import (
        audit_second_source_bound_hopf,
    )
    report = audit_second_source_bound_hopf()
    assert report["scoped_search_complete"] is True
    assert report["trust_boundary_accepted"] is True
    assert report["new_given_added"] == 0
