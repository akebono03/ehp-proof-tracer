"""Goal-only boundary using the registered recursive proof engine.

No historical replay or per-group premise pool may be supplied. The default
production invocation remains fail-closed until a vetted registry and a
rule-expansion catalog are connected.
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
    """Use registered recursive search, refusing any missing input.

    Legacy callers with only n and k fail closed. Supplying a goal, a genuine
    registry, a citing assertion and a common expansion catalog enables the
    recursive engine, without preselected ProofSteps or a fallback.
    """
    group = TodaPrimaryGroup(group_dimension=n + k, sphere_dimension=n)
    if (
        goal is None
        or bridge is None
        or citing_assertion_id is None
        or expansion_provider is None
    ):
        raise GoalSearchIncompleteError(
            f"Registered goal/rule catalog not configured for {group!r}; "
            "legacy proof selection remains disabled"
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
