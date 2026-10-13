"""Phase 164 R5-R2: select a proof replay, never render text here.

All selected replays must pass through the same presentation and renderer.
Legacy proof construction is explicitly disabled by Phase 165.
"""


def build_phase164_r5_r2_common_replay(n: int, k: int, group_result, max_depth: int, mode: str):
    """Fail closed until a verified typed registry and common rule catalog are connected.

    No old repository replay, group-specific reconstruction, or stable-eta
    replay is an acceptable proof source in the unified Web proof route.
    """
    if n == 2 and k == 1:
        from phase165_r14_r40_replay import build_phase165_r40_pi32_common_replay
        return build_phase165_r40_pi32_common_replay(group_result, max_depth)

    from phase165_goal_only_search import GoalSearchIncompleteError

    raise GoalSearchIncompleteError(
        "Registered goal/rule catalog not configured for "
        f"group (n={n}, k={k}); legacy proof selection remains disabled"
    )
