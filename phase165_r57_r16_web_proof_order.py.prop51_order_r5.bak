"""R57-R16: reviewed, finite proof-use order metadata for ordinary Web queries.

This is NOT publication order, a proof assertion, or a derived group result.
Group structures are selected afresh from the typed registry. No completed
ProofStep is persisted. Unreviewed/missing/ambiguous order is fail-closed.
"""
from __future__ import annotations

from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog, ProofOrderRecord


# Agreed proof-development order. These are (sphere dimension, stem), NOT
# stored group answers; expanding this table requires separate review.
REVIEWED_PROOF_TARGET_ORDER: tuple[tuple[int, int], ...] = (
    (2, 1),  # pi_3^2
    (3, 1),  # pi_4^3
    (4, 1),  # pi_5^4
)


def resolve_reviewed_order_catalog(bridge, *, n: int, k: int):
    """Return a position-only catalog or a diagnostic, with no fake premises.

    Queries not covered by an explicit reviewed order retain ordinary shared
    search without a recursive catalog. Missing earlier typed goals prevent
    granting reviewed reuse; no structure is guessed from (n,k).
    """
    key = (n, k)
    if key not in REVIEWED_PROOF_TARGET_ORDER:
        return None, None
    from phase165_r55_nk_only_goal import registered_group_goal_candidates

    target_index = REVIEWED_PROOF_TARGET_ORDER.index(key)
    catalog = ProofOrderCatalog()
    for position, (source_n, source_k) in enumerate(
        REVIEWED_PROOF_TARGET_ORDER[:target_index + 1]
    ):
        candidates = registered_group_goal_candidates(
            bridge, n=source_n, k=source_k,
        )
        if len(candidates) != 1:
            reason = ("型付き証明目標が未登録" if not candidates
                      else "型付き証明目標が複数存在")
            return None, (
                "先行証明の順序データを適用できません: "
                f"π_{source_n + source_k}^{source_n} の{reason}"
            )
        catalog.register(ProofOrderRecord(
            statement=candidates[0], position=position,
        ))
    return catalog, None
