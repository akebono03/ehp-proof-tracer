"""R4R5R3 general source-first backward-provider contracts (test shapes only)."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from expression import GeneratorSymbol, HomotopyElement, Multiple, Zero
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase175_r4r5r3_public_order_zero import provider
from phase175_r4r5_eta7_annihilator_isolated.rule import RULE_NAME
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def component(n: int, k: int = 1, label: str = "a") -> HomotopyElement:
    return HomotopyElement(label, n, source=n+k, target=n,
                           generator=GeneratorSymbol(label, index=n))


def sample_goal(generator: HomotopyElement, order: int) -> Relation:
    return Relation(Multiple(order, generator), Zero(), RelationType.EQUALITY)


def prior_root() -> Relation:
    return Relation(TodaPrimaryGroup(9, 5), FiniteCyclicGroup(2, component(5, 4)))


@dataclass(frozen=True)
class FakeAssertion:
    origin: object
    content: object


@dataclass(frozen=True)
class FakeLink:
    assertion_id: str
    step: object


class FakeRegistry:
    def __init__(self, source: Relation, origin=AssertionOrigin.FIXED_STATEMENT):
        self.record = FakeAssertion(origin, source)

    def assertion(self, ident: str) -> FakeAssertion:
        assert ident == "fixed"
        return self.record


class FakeBridge:
    def __init__(self, source: Relation, *, origin=AssertionOrigin.FIXED_STATEMENT,
                 proof_rule=ProofRule.GIVEN):
        self.registry = FakeRegistry(source, origin)
        self.proof_links = (FakeLink("fixed", ProofStep(source, (), proof_rule)),)


def test_public_provider_uses_direct_sum_actual_component(monkeypatch) -> None:
    a, b = component(4, 4, "a"), component(4, 4, "b")
    source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((
        FiniteCyclicGroup(2, a), FiniteCyclicGroup(4, b),
    )))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: None)
    expand = provider.build_public_order_zero_provider(
        bridge=FakeBridge(source), proof_target=prior_root(),
    )
    for g, order in ((a, 2), (b, 4)):
        options = expand(sample_goal(g, order))
        assert len(options) == 1
        assert options[0].subgoals == (source,)
        assert options[0].rule.name == RULE_NAME
    assert expand(sample_goal(a, 4)) == ()
    assert expand(sample_goal(component(4, 4, "unrelated"), 2)) == ()


def test_public_provider_prior_conclusions_have_same_general_semantics(monkeypatch) -> None:
    a = component(4, 4)
    source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((
        FreeCyclicGroup(component(4, 4, "free")),
        FiniteCyclicGroup(6, a),
    )))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: None)
    expand = provider.build_public_order_zero_provider(
        bridge=object(), proof_target=prior_root(), prior_conclusions=(source,),
    )
    proposals = expand(sample_goal(a, 6))
    assert len(proposals) == 1 and proposals[0].subgoals == (source,)


def test_public_provider_db_only_never_returns_a_proof_step(monkeypatch) -> None:
    a = component(7)
    source = Relation(TodaPrimaryGroup(8, 7), FiniteCyclicGroup(2, a))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: source)
    expand = provider.build_public_order_zero_provider(
        bridge=object(), proof_target=prior_root(),
    )
    options = expand(sample_goal(a, 2))
    assert len(options) == 1
    assert options[0].subgoals == (source,)
    assert options[0].rule.premise_patterns[0].statement_pattern == source
    assert options[0].rule.premise_patterns[0].proof_rule is None


def test_unverified_or_unordered_source_is_not_proposed(monkeypatch) -> None:
    a = component(4, 4)
    source = Relation(TodaPrimaryGroup(8, 4), FiniteCyclicGroup(2, a))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: None)
    for bridge in (FakeBridge(source, origin=object()),
                   FakeBridge(source, proof_rule=ProofRule.RELATION)):
        expand = provider.build_public_order_zero_provider(
            bridge=bridge, proof_target=prior_root(),
        )
        assert expand(sample_goal(a, 2)) == ()
    earlier_root = Relation(TodaPrimaryGroup(7, 3), FiniteCyclicGroup(2, component(3, 4)))
    expand = provider.build_public_order_zero_provider(
        bridge=FakeBridge(source), proof_target=earlier_root,
    )
    assert expand(sample_goal(a, 2)) == ()


def test_wrong_root_goal_and_wrong_goal_type_are_inert(monkeypatch) -> None:
    a = component(7)
    source = Relation(TodaPrimaryGroup(8, 7), FiniteCyclicGroup(2, a))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: source)
    for root in (None, "pi_9^5", Relation(Multiple(2, a), Zero())):
        assert provider.build_public_order_zero_provider(
            bridge=object(), proof_target=root,
        )(sample_goal(a, 2)) == ()
    expand = provider.build_public_order_zero_provider(
        bridge=object(), proof_target=prior_root(),
    )
    assert expand(Relation(Multiple(2, a), a)) == ()
    assert expand(Relation(Multiple(2, a), Zero(), RelationType.ORDER)) == ()


def test_candidate_mismatch_not_sufficient(monkeypatch) -> None:
    a = component(4, 4)
    bad = Relation(TodaPrimaryGroup(8, 4), FiniteCyclicGroup(4, a))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: bad)
    expand = provider.build_public_order_zero_provider(
        bridge=object(), proof_target=prior_root(),
    )
    assert expand(sample_goal(a, 2)) == ()


def test_duplicate_concrete_sources_are_deduplicated(monkeypatch) -> None:
    a = component(4, 4)
    source = Relation(TodaPrimaryGroup(8, 4), FiniteCyclicGroup(2, a))
    monkeypatch.setattr(provider, "exact_prior_database_result", lambda n, k: source)
    expand = provider.build_public_order_zero_provider(
        bridge=FakeBridge(source), proof_target=prior_root(),
        prior_conclusions=(source,),
    )
    assert len(expand(sample_goal(a, 2))) == 1


def test_empty_prior_conclusions_is_tuple_only() -> None:
    with pytest.raises(TypeError, match="must be a tuple"):
        provider.build_public_order_zero_provider(
            bridge=object(), proof_target=prior_root(), prior_conclusions=[],
        )
