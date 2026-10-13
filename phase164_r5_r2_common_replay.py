"""Phase 164 R5-R2: select dynamically reconstructed registered proofs.

No legacy replay fallback, and no group-specific proof-selection branch.
All supported proofs go through the common presentation and renderer.
"""
from __future__ import annotations

from phase165_r52_r7_registered_common_proof import build_registered_common_replay


def build_phase164_r5_r2_common_replay(
    n: int, k: int, group_result, max_depth: int, mode: str,
):
    """Dispatch by matching a typed mathematical Goal, never by n/k cases."""
    if group_result.target.group_dimension != n + k or group_result.target.sphere_dimension != n:
        raise ValueError("group result does not match requested n, k")
    return build_registered_common_replay(
        group_result=group_result, max_depth=max_depth, mode=mode,
    )
