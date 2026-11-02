"""Focused proof-contract tests using actual EHP Proof Tracer types."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, MapApplication
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase173_r4_r1_source_bound_56.rule import (
    _target_generators, source_bound_toda56_rule,
    expand_source_bound_toda56,
)
from proof import ProofRule, Relation, RelationType
from toda_rules import EHP_H_MAP


def fixture_relations():
    nu4 = HomotopyElement(
        name="ν₄", dimension=4, source=7, target=4,
        generator=GeneratorSymbol(family="ν", index=4),
    )
    prime = HomotopyElement(
        name="ν'", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="\\nu'", index=None),
    )
    iota = HomotopyElement(
        name="ι_7", dimension=7, generator=GeneratorSymbol(family="ι", index=7),
    )
    goal = Relation(
        TodaPrimaryGroup(7, 4),
        DirectSumGroup((FreeCyclicGroup(nu4),
                        FiniteCyclicGroup(4, IteratedSuspension(prime, 1)))),
        RelationType.EQUALITY,
    )
    prior = Relation(TodaPrimaryGroup(6, 3), FiniteCyclicGroup(4, prime), RelationType.EQUALITY)
    diagonal = Relation(TodaPrimaryGroup(7, 7), FreeCyclicGroup(iota), RelationType.EQUALITY)
    hopf = Relation(MapApplication(EHP_H_MAP, nu4), iota, RelationType.EQUALITY)
    return goal, prior, diagonal, hopf


def test_exact_target_is_typed() -> None:
    goal, prior, diagonal, hopf = fixture_relations()
    assert _target_generators(goal) is not None
    assert source_bound_toda56_rule(goal, prior, diagonal, hopf).conclusion_pattern == goal


def test_wrong_prime_generator_is_rejected() -> None:
    goal, prior, diagonal, hopf = fixture_relations()
    wrong = Relation(prior.lhs, FiniteCyclicGroup(4, goal.rhs.summands[0].generator), RelationType.EQUALITY)
    with pytest.raises(ValueError):
        source_bound_toda56_rule(goal, wrong, diagonal, hopf)


def test_wrong_hopf_image_is_rejected() -> None:
    goal, prior, diagonal, hopf = fixture_relations()
    wrong = Relation(hopf.lhs, goal.rhs.summands[0].generator, RelationType.EQUALITY)
    with pytest.raises(ValueError):
        source_bound_toda56_rule(goal, prior, diagonal, wrong)


def test_rule_requires_given_source_and_derived_hopf() -> None:
    goal, prior, diagonal, hopf = fixture_relations()
    rule = source_bound_toda56_rule(goal, prior, diagonal, hopf)
    steps = (
        SimpleNamespace(conclusion=TodaProp44UniversalStatement(), rule=ProofRule.GIVEN),
        SimpleNamespace(conclusion=prior, rule=ProofRule.INFERENCE),
        SimpleNamespace(conclusion=diagonal, rule=ProofRule.INFERENCE),
        SimpleNamespace(conclusion=hopf, rule=ProofRule.INFERENCE),
    )
    assert rule.match_guard(steps, {}) is True
    replaced = (*steps[:3], SimpleNamespace(conclusion=hopf, rule=ProofRule.GIVEN))
    assert rule.match_guard(replaced, {}) is False


def test_no_citation_means_no_root(monkeypatch) -> None:
    goal, prior, diagonal, hopf = fixture_relations()
    assert expand_source_bound_toda56(
        goal, (), object(), proof_target=goal,
    ) == ()


def test_no_root_for_other_group() -> None:
    goal, prior, diagonal, hopf = fixture_relations()
    other = Relation(TodaPrimaryGroup(8, 5), goal.rhs, RelationType.EQUALITY)
    assert _target_generators(other) is None
