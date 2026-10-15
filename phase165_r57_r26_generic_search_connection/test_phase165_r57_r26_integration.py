"""R26 wiring checks: no new GIVEN or forged proof assertions."""
from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
import phase165_r52_r9_shared_math as shared
import phase165_r57_r26_generic_search_connection as generic
from proof import InferenceRule
from unified_statement_registry import UnifiedStatementRegistry


@dataclass(frozen=True)
class SyntheticGoal:
    value: int


def test_r26_shared_provider_emits_generic_proposals(monkeypatch):
    rule = InferenceRule("synthetic goal")
    calls = []

    def factory(rules=None):
        calls.append("build")
        return lambda goal: (GoalExpansion(rule, (SyntheticGoal(goal.value - 1),)),) if isinstance(goal, SyntheticGoal) else ()

    monkeypatch.setattr(generic, "build_generic_backward_expansion_provider", factory)
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    provider = shared.shared_expansion_provider(bridge)
    assert provider(SyntheticGoal(4)) == (GoalExpansion(rule, (SyntheticGoal(3),)),)
    assert calls == ["build"]


def test_r26_searcher_itself_is_unchanged():
    import inspect
    from phase165_r3_recursive_search import reconstruct_registered_goal
    source = inspect.getsource(reconstruct_registered_goal)
    assert "find_inference_matches_for_rule" in source
    assert "derive_inference_proof_step" in source
    assert "phase165_r57_r26" not in source
