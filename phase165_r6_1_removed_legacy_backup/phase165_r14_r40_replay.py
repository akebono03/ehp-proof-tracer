"""Historical R40 entry delegates to the sole common proof search."""
from __future__ import annotations

from phase165_r52_r7_registered_common_proof import build_registered_common_replay


def build_phase165_r40_pi32_common_replay(group_result, max_depth: int):
    """Compatibility entry: no group-specific proof reconstruction."""
    return build_registered_common_replay(
        group_result=group_result, max_depth=max_depth, mode="trace",
    )
