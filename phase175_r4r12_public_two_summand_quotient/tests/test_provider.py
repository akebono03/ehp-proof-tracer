"""Regression: existing generic rank-two quotient is only an unproved proposal."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase175_r4r3_two_summand_quotient.rule import (
    RULE_NAME, two_summand_quotient_inputs,
)
from phase175_r4r3_two_summand_quotient.tests.test_rule import fixture
from phase175_r4r12_public_two_summand_quotient.provider import (
    ordered_summand_inputs,
    expand_public_two_summand_quotient,
    build_public_two_summand_quotient_provider,
)
from proof import ProofStep, Relation, RelationType


def sample():
    goal, domain, delta_source, delta_image, suspension_image = fixture()
    root = Relation(goal.group, FiniteCyclicGroup(2, goal.generator))
    prior = {(4, 4): domain, (9, 1): delta_source}
    calls = []

    def lookup(n: int, k: int):
        calls.append((n, k))
        return prior.get((n, k))

    return goal, root, domain, delta_source, lookup, calls


def test_only_two_earlier_db_candidates_are_read() -> None:
    goal, root, middle, source, lookup, calls = sample()
    assert ordered_summand_inputs(goal, proof_target=root, database_lookup=lookup) == (
        middle, source,
    )
    assert calls == [(4, 4), (9, 1)]


def test_two_conditional_routes_preserve_all_six_obligations() -> None:
    goal, root, middle, source, lookup, _ = sample()
    routes = expand_public_two_summand_quotient(
        goal, proof_target=root, database_lookup=lookup,
    )
    assert len(routes) == 2
    assert all(route.rule.name == RULE_NAME for route in routes)
    for option in routes:
        required = option.subgoals
        assert len(required) == 6
        assert required[:2] == (middle, source)
        assert not any(isinstance(item, ProofStep) for item in required)
        assert two_summand_quotient_inputs(
            goal, middle, source, required[2], required[5],
        ) == required
    assert {route.subgoals[2].target_generator for route in routes} == {
        part.generator for part in middle.rhs.summands
    }


def test_proof_target_must_match_actual_group_and_generator() -> None:
    goal, root, _, _, lookup, calls = sample()
    assert not expand_public_two_summand_quotient(
        goal, proof_target=replace(root, lhs=TodaPrimaryGroup(9, 6)),
        database_lookup=lookup,
    )
    assert not expand_public_two_summand_quotient(
        replace(goal, order=4), proof_target=root, database_lookup=lookup,
    )
    assert not expand_public_two_summand_quotient(
        goal, proof_target=None, database_lookup=lookup,
    )
    assert not calls


def test_incomplete_or_forged_prior_data_is_rejected() -> None:
    goal, root, middle, source, lookup, _ = sample()
    malformed = replace(middle, rhs=DirectSumGroup((
        FiniteCyclicGroup(4, middle.rhs.summands[0].generator),
        middle.rhs.summands[1],
    )))
    assert not expand_public_two_summand_quotient(
        goal, proof_target=root,
        database_lookup=lambda n, k: malformed if (n, k) == (4, 4) else source,
    )
    assert not expand_public_two_summand_quotient(
        goal, proof_target=root,
        database_lookup=lambda n, k: middle if (n, k) == (4, 4) else None,
    )
    bad_delta = replace(source, rhs=FiniteCyclicGroup(4, source.rhs.generator))
    assert not expand_public_two_summand_quotient(
        goal, proof_target=root,
        database_lookup=lambda n, k: middle if (n, k) == (4, 4) else bad_delta,
    )


def test_group_relation_is_never_accepted_directly_as_cyclic_goal() -> None:
    goal, root, _, _, lookup, calls = sample()
    assert not expand_public_two_summand_quotient(
        root, proof_target=root, database_lookup=lookup,
    )
    assert not calls


def test_unrelated_concrete_root_is_not_searched_as_earlier_db_prior() -> None:
    goal, root, _, _, lookup, _ = sample()
    target = replace(goal, group=TodaPrimaryGroup(7, 5))
    assert not expand_public_two_summand_quotient(
        target, proof_target=root, database_lookup=lookup,
    )


def test_real_public_builder_does_not_materialize_proof() -> None:
    goal, root, _, _, _, _ = sample()
    factory = build_public_two_summand_quotient_provider(proof_target=root)
    assert callable(factory)
    assert factory("untyped literature text") == ()
    # Under real repository data the two authenticated DB rows are obtained
    # dynamically; proposals remain unproved until the ordinary resolver runs.
    assert all(not isinstance(exp, ProofStep) for exp in factory(goal))
