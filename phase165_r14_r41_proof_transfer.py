"""Phase 165 R41: preserve complete registered ancestry for pi3^2 narratives."""
from __future__ import annotations

from pathlib import Path

from phase165_r14_r38_direct_registry import reconstruct_registered_pi32
from phase165_r14_r40_replay import build_phase165_r40_pi32_common_replay
from toda_proof_dependency import extract_toda_recursive_proof_provenance
from toda_group_result_proof_replay import build_toda_group_result_proof_replay


def _registered_reference_leaves(root):
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
    """Use R40 replay adapter but never truncate narrative inference ancestry."""
    replay = build_phase165_r40_pi32_common_replay(group_result, max_depth)
    if mode != "narrative":
        return replay
    _, registered_root = reconstruct_registered_pi32(
        Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
    )
    if replay.root_step.conclusion != registered_root.conclusion:
        raise ValueError("replay root disagrees with registered backward proof")
    registered_leaves = _registered_reference_leaves(registered_root)
    if len(registered_leaves) != 9:
        raise ValueError("R38 frontier does not have nine reference leaves")
    replay_leaves = _registered_reference_leaves(replay.root_step)
    if len(replay_leaves) != len(registered_leaves):
        raise ValueError("reference leaves lost in replay conversion")
    for leaf in registered_leaves:
        if not any(type(leaf.conclusion) is type(other.conclusion)
                   and leaf.conclusion == other.conclusion for other in replay_leaves):
            raise ValueError("registered reference was lost")
    provenance = extract_toda_recursive_proof_provenance(replay.group_result)
    full_depth = max(node.shortest_depth for node in provenance.nodes)
    return build_toda_group_result_proof_replay(
        replay.group_result, max_depth=max(max_depth, full_depth),
    )


def audit_r41(group_result):
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
