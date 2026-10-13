"""R52-R2 deterministic adapter checks; no Toda computation implied."""
from dataclasses import dataclass

import pytest

import phase165_r52_r2_search_adapter as adapter
from phase165_r3_recursive_search import RegisteredGoalUnresolved
from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from homotopy_groups import TodaPrimaryGroup
from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class SyntheticStatement:
    lhs: object


def test_r52_r2_unconfigured_remains_not_searched():
    result = adapter.search_registered_partial_proof(n=500, k=111, goal="missing")
    assert result.status is ProofSearchStatus.NOT_SEARCHED
    assert result.open_goals == ("missing",)
    assert result.proven_steps == ()


def test_r52_r2_partial_preserves_proved_leaf(monkeypatch):
    leaf = ProofStep(conclusion="premise", premises=(), rule=ProofRule.GIVEN)
    root = SyntheticStatement(TodaPrimaryGroup(9, 6))

    def fake_reconstruct(goal, bridge, cite, provider, *, verified_assertion_ids, lookup_mode, progress_observer):
        progress_observer("proved", "premise", leaf)
        progress_observer("unresolved", "missing", None)
        raise RegisteredGoalUnresolved("missing rule")

    monkeypatch.setattr(adapter, "reconstruct_registered_goal", fake_reconstruct)
    result = adapter.search_registered_partial_proof(
        n=6, k=3, goal=root, bridge=object(), citing_assertion_id="c",
        expansion_provider=lambda _: (),
    )
    assert result.status is ProofSearchStatus.PARTIAL
    assert result.proven_steps == (leaf,)
    assert "missing" in result.open_goals
    assert root in result.open_goals
    assert "□" not in render_partial_proof_markdown(result)


def test_r52_r2_no_steps_is_failed(monkeypatch):
    def fake_reconstruct(goal, bridge, cite, provider, *, verified_assertion_ids, lookup_mode, progress_observer):
        raise RegisteredGoalUnresolved("no registered derivation")

    monkeypatch.setattr(adapter, "reconstruct_registered_goal", fake_reconstruct)
    result = adapter.search_registered_partial_proof(
        n=3, k=2, goal="unresolved", bridge=object(),
        citing_assertion_id="c", expansion_provider=lambda _: (),
    )
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.open_goals == ("unresolved",)
    assert result.diagnostics == ("no registered derivation",)


def test_r52_r2_canonical_success_is_complete_only_for_target(monkeypatch):
    target = SyntheticStatement(TodaPrimaryGroup(1002, 1000))
    step = ProofStep(conclusion=target, premises=(), rule=ProofRule.GIVEN)

    def fake_reconstruct(goal, bridge, cite, provider, *, verified_assertion_ids, lookup_mode, progress_observer):
        progress_observer("proved", goal, step)
        return step

    monkeypatch.setattr(adapter, "reconstruct_registered_goal", fake_reconstruct)
    args = dict(n=1000, k=2, goal=target, bridge=object(), citing_assertion_id="c", expansion_provider=lambda _: ())
    result = adapter.search_registered_partial_proof(**args)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == target
    assert "□" in render_partial_proof_markdown(result)
    other = adapter.search_registered_partial_proof(**{**args, "n": 999})
    assert other.status is ProofSearchStatus.PARTIAL
    assert other.conclusion is None


def test_r52_r2_rejects_invalid_range_even_not_searched():
    with pytest.raises(ValueError):
        adapter.search_registered_partial_proof(n=1, k=0)
