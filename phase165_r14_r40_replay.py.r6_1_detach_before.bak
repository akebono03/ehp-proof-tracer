"""Adapt the R38 registered proof to the existing common replay pipeline."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from phase165_r14_r38_direct_registry import reconstruct_registered_pi32
from toda_group_result_proof_replay import build_toda_group_result_proof_replay


def build_phase165_r40_pi32_common_replay(group_result, max_depth: int):
    """Preserve the existing group result, replacing only its proof root."""
    if isinstance(max_depth, bool) or not isinstance(max_depth, int) or max_depth < 0:
        raise ValueError("max_depth must be a nonnegative integer")
    tex = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
    _, proof = reconstruct_registered_pi32(tex)
    if (getattr(proof.conclusion, "lhs", None) != group_result.target
            or getattr(proof.conclusion, "rhs", None) != group_result.group_structure):
        raise ValueError("registered proof group structure differs from displayed group result")
    source_entry = replace(
        group_result.source_entry,
        key="phase165:registered:pi3_2",
        step=proof,
        phase="165",
        theorem="Toda (5.1); Proposition 4.2; Proposition 5.1",
    )
    adapted_group_result = replace(
        group_result, source_entry=source_entry, proof_step=proof,
    )
    return build_toda_group_result_proof_replay(
        adapted_group_result, max_depth=max_depth,
    )
