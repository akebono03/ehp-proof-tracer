"""Historical R41 calls share the production backward-search entry."""
from __future__ import annotations

from phase165_r52_r7_registered_common_proof import build_registered_common_replay


def _registered_reference_leaves(root):
    """Collect terminal proof steps independently of a particular group."""
    seen = set()
    leaves = []

    def visit(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        if not step.premises:
            leaves.append(step)
            return
        for child in step.premises:
            visit(child)

    visit(root)
    return tuple(leaves)


def build_phase165_r41_pi32_common_replay(group_result, max_depth: int, mode: str):
    """Compatibility entry: no specialized proof reconstruction."""
    return build_registered_common_replay(
        group_result=group_result, max_depth=max_depth, mode=mode,
    )


def audit_r41(group_result):
    """Historical audit of proof preservation through the common renderer."""
    trace = build_phase165_r41_pi32_common_replay(group_result, 2, "trace")
    narrative = build_phase165_r41_pi32_common_replay(group_result, 2, "narrative")
    return {
        "phase": "165 R14-R41",
        "root_equal": trace.root_step.conclusion == narrative.root_step.conclusion,
        "full_registered_leaf_count": len(_registered_reference_leaves(narrative.root_step)),
        "trace_nodes_depth2": len(trace.steps),
        "narrative_nodes_complete": len(narrative.steps),
        "narrative_max_depth": narrative.max_depth,
        "narrative_uses_common_renderer": True,
        "reference_text_rendering_fixed": False,
        "full_pytest_run": False,
    }
