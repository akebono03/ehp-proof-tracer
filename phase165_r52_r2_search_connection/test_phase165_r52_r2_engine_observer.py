"""R52-R2 live recursive search observer test, using synthetic assertions."""
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import (
    GoalExpansion,
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def test_r52_r2_engine_reports_proven_branch_and_open_goal(monkeypatch):
    import phase165_r3_recursive_search as engine

    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "src", ReferenceKind.PROPOSITION, "Synthetic source",
        source_id="synthetic", publication_position=1,
    ))
    registry.add_assertion(AssertionEntry(
        "source", "src", AssertionKind.STATEMENT, "root",
    ))
    bridge = RegistryBridgeResult(registry, (), ())
    proven_leaf = ProofStep(conclusion="known", premises=(), rule=ProofRule.GIVEN)
    monkeypatch.setattr(
        engine, "_typed_reference_steps",
        lambda bridge, goal: (proven_leaf,) if goal == "known" else (),
    )
    observed = []

    def provider(goal):
        if goal == "root":
            return (GoalExpansion(object(), ("known", "unknown")),)
        return ()

    try:
        reconstruct_registered_goal(
            "root", bridge, "source", provider,
            lookup_mode="typed_reference",
            progress_observer=lambda event, goal, step: observed.append((event, goal, step)),
        )
    except RegisteredGoalUnresolved:
        pass
    else:
        raise AssertionError("unresolved root must remain unresolved")
    assert ("proved", "known", proven_leaf) in observed
    assert ("unresolved", "unknown", None) in observed
    assert ("unresolved", "root", None) in observed
