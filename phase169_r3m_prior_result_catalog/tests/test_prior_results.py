"""Focused tests for the proof-status-independent prior-result catalog."""
from __future__ import annotations

import inspect

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase169_r3m_prior_result_catalog import prior_results
from proof import Relation, RelationType
from homotopy_groups import TodaPrimaryGroup, FiniteCyclicGroup
from expression import HomotopyElement, GeneratorSymbol
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ReferenceKind, UnifiedStatementRegistry,
)


def _relation(n: int) -> Relation:
    return Relation(
        TodaPrimaryGroup(n + 2, n),
        FiniteCyclicGroup(2, HomotopyElement(
            name="eta", dimension=n, source=n + 2, target=n,
            generator=GeneratorSymbol(family="eta", index=n),
        )),
        RelationType.EQUALITY,
    )


def _bridge(*, source_position: int = 6000):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "source", ReferenceKind.PROPOSITION, "Proposition X",
        publication_position=source_position,
    ))
    registry.add_reference(LiteratureEntry(
        "target", ReferenceKind.PROPOSITION, "Proposition Y",
        publication_position=7000,
    ))
    registry.add_assertion(AssertionEntry(
        "source_id", "source", AssertionKind.STATEMENT,
        _relation(3), origin=AssertionOrigin.FIXED_STATEMENT,
        component_position=100,
    ))
    registry.add_assertion(AssertionEntry(
        "target_id", "target", AssertionKind.STATEMENT,
        _relation(4), origin=AssertionOrigin.FIXED_STATEMENT,
        component_position=200,
    ))
    return RegistryBridgeResult(registry, (), ())


def _stub_result(monkeypatch):
    relation = _relation(3)
    monkeypatch.setattr(prior_results, "_database_result_candidates",
                        lambda **kwargs: (relation,))
    import phase166_r3t_goal_source_binding.goal_source as source
    monkeypatch.setattr(source, "resolve_specialized_goal_citing_id",
                        lambda bridge, goal: "source_id")


def test_earlier_result_available_with_no_completed_proof(monkeypatch):
    _stub_result(monkeypatch)
    bridge = _bridge()  # No ProofStepLink, completed proof or proof repository.
    result = prior_results.resolve_prior_group_result(
        bridge, source_n=3, source_k=2, citing_assertion_id="target_id",
    )
    assert result.eligible is True
    assert result.reason == "prior_fixed_source"
    assert result.relation == _relation(3)
    assert result.source_assertion_id == "source_id"
    assert bridge.proof_links == ()


def test_later_source_is_not_prior(monkeypatch):
    _stub_result(monkeypatch)
    bridge = _bridge(source_position=8000)
    assert bridge.registry.reference("source").publication_position > bridge.registry.reference("target").publication_position
    result = prior_results.resolve_prior_group_result(
        bridge, source_n=3, source_k=2, citing_assertion_id="target_id",
    )
    assert result.eligible is False
    assert result.reason == "source_not_prior"


def test_same_group_as_target_is_rejected(monkeypatch):
    """The DB mock must refer to the very same group as the target."""
    same_group = _relation(4)
    monkeypatch.setattr(
        prior_results,
        "_database_result_candidates",
        lambda **kwargs: (same_group,),
    )
    result = prior_results.resolve_prior_group_result(
        _bridge(), source_n=4, source_k=2, citing_assertion_id="target_id",
    )
    assert result.relation == same_group
    assert result.source_assertion_id is None
    assert result.eligible is False
    assert result.reason == "same_group_as_target"


def test_unpositioned_database_result_remains_data_not_proof(monkeypatch):
    _stub_result(monkeypatch)
    import phase166_r3t_goal_source_binding.goal_source as source
    monkeypatch.setattr(source, "resolve_specialized_goal_citing_id",
                        lambda bridge, goal: None)
    result = prior_results.resolve_prior_group_result(
        _bridge(), source_n=3, source_k=2, citing_assertion_id="target_id",
    )
    assert result.relation == _relation(3)
    assert not result.eligible
    assert result.reason == "source_not_uniquely_positioned"


def test_missing_data_never_yields_an_assertion(monkeypatch):
    monkeypatch.setattr(prior_results, "_database_result_candidates",
                        lambda **kwargs: ())
    result = prior_results.resolve_prior_group_result(
        _bridge(), source_n=3, source_k=2, citing_assertion_id="target_id",
    )
    assert result.relation is None
    assert result.source_assertion_id is None
    assert not result.eligible


def test_prior_result_module_does_not_consult_proof_status():
    source = inspect.getsource(prior_results)
    for forbidden in (
        "CompletedInternalProof", "ProofSearchStatus", "proven_steps",
        "search_shared_group_goal", "reconstruct_registered_goal",
    ):
        assert forbidden not in source
