"""Goal-only search boundary; never substitute historical proof replays.

This phase deliberately refuses unimplemented registry-to-goal search instead
of silently importing specialized, preselected ProofStep trees.
"""
from homotopy_groups import TodaPrimaryGroup


class GoalSearchIncompleteError(RuntimeError):
    """The registered rules do not yet establish the requested goal."""


def construct_registered_group_proof(*, n: int, k: int):
    """Require the common registry-backed goal-only backend.

    No preselected premise pool, existing group result, or historical replay
    is accepted. The current repository has only leaf-supplied reconstruction
    for pi_5^3; refusing that path is intentional.
    """
    goal_group = TodaPrimaryGroup(group_dimension=n + k, sphere_dimension=n)
    raise GoalSearchIncompleteError(
        "Goal-only registered premise discovery is not implemented for "
        f"{goal_group!r}; legacy proof selection is disabled"
    )
