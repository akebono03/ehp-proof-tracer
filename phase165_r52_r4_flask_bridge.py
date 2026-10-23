"""R52-R5: Flask bridge for automatically initiated typed searches.

An explicit goal continues to use the R52-R4 search contract unchanged.
When none is supplied the production registry and rule catalog are discovered,
and a new goal search is executed (without legacy proof replay).
"""
from __future__ import annotations

from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase165_r52_r5_auto_search import search_group_structure_automatically


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
    """Route the ordinary Flask group proof through the model-backed public entry.

    Explicit proof-search inputs retain the existing typed partial-result contract.
    """
    if (
        goal is None
        and bridge is None
        and citing_assertion_id is None
        and expansion_provider is None
        and not verified_assertion_ids
    ):
        from web_group_proof import build_standard_web_group_proof_view

        return build_standard_web_group_proof_view(
            n=n,
            k=k,
            max_depth=max_depth,
            mode="narrative",
            citation_source="model",
        )

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
