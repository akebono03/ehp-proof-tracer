"""Run the real ordinary group query after the one-function install."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result


def test_pi73_ordinary_search_proves_exact_registered_goal() -> None:
    target = exact_prior_database_result(3, 4)
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=4, bridge=build_shared_typed_bridge(),
        context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == target
    assert len(result.open_goals) == 0
    assert len(result.proven_steps) > 0
    assert len(contexts) == 1
