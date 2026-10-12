"""Production Goal-only boundary with common R3 and R8 engines.

Registry/rule discovery is automatic; no target-specific premise pool or replay.
Citation eligibility remains fail-closed and no source statement is approved.
"""
from homotopy_groups import TodaPrimaryGroup
from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)


class GoalSearchIncompleteError(RuntimeError):
    """A goal cannot be established by the configured common search."""


def construct_registered_group_proof(
    *,
    n: int,
    k: int,
    goal=None,
    bridge=None,
    citing_assertion_id=None,
    expansion_provider=None,
    verified_assertion_ids=(),
):
    """Discover common production inputs unless an explicit input is provided.

    Missing goal/citation context is not inferred from the target dimensions;
    such inference would amount to assuming the desired result. The existing
    explicit-input API is preserved for independently reviewed citations.
    """
    group = TodaPrimaryGroup(group_dimension=n + k, sphere_dimension=n)
    if bridge is None or expansion_provider is None:
        from phase165_r9_production_wiring import discover_goal_search_inputs
        inputs = discover_goal_search_inputs()
        if bridge is None:
            bridge = inputs.bridge
        if expansion_provider is None:
            expansion_provider = inputs.expansion_provider
    if goal is None or citing_assertion_id is None:
        raise GoalSearchIncompleteError(
            f"Registered goal/citation context not configured for {group!r}; "
            "legacy proof selection is disabled"
        )
    try:
        step = reconstruct_registered_goal(
            goal,
            bridge,
            citing_assertion_id,
            expansion_provider,
            verified_assertion_ids=verified_assertion_ids,
        )
    except RegisteredGoalUnresolved as exc:
        raise GoalSearchIncompleteError(str(exc)) from exc
    if getattr(getattr(step, "conclusion", None), "lhs", None) != group:
        raise GoalSearchIncompleteError("derived proof targets a different group")
    return step
