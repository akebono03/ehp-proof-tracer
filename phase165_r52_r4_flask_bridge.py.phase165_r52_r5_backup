"""R52-R4: Flask-independent bridge from registered search to the common Web view.

Do not invent a mathematical goal from a pair of indices. Missing search input
is displayed as NOT_SEARCHED. An equipped caller may pass a genuine typed goal,
registry bridge and rule catalog to execute the existing observer-enabled search.
"""
from __future__ import annotations

from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view


def build_group_proof_progress_view(
    *,
    n: int,
    k: int,
    max_depth: int = 2,
    goal: object | None = None,
    bridge: object | None = None,
    citing_assertion_id: str | None = None,
    expansion_provider: object | None = None,
    verified_assertion_ids: tuple[str, ...] = (),
):
    """Render an observed search state; never silently claim a proof exists."""
    result = search_registered_partial_proof(
        n=n,
        k=k,
        goal=goal,
        bridge=bridge,
        citing_assertion_id=citing_assertion_id,
        expansion_provider=expansion_provider,
        verified_assertion_ids=verified_assertion_ids,
    )
    return build_partial_web_group_proof_view(
        result,
        max_depth=max_depth,
        mode="narrative",
    )
