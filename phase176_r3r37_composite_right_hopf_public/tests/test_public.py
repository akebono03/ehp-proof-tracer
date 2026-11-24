"""Live shared-provider integration in the user's source-first checkout."""
from __future__ import annotations

from phase176_r3r37_composite_right_hopf_public.audit import probe


def test_screened_composite_formula_substitution_and_old_branches() -> None:
    result = probe()
    assert result["gate"] == "PASS_R3R37_PUBLIC_COMPOSITE_HOPF_CONNECTED"
    assert result["public_formula_candidate_count"] == 1
    assert result["public_substitution_candidate_count"] == 1
    assert result["public_substitution_subgoals"] == 2
    assert result["local_formula_replayed"] is True
    assert result["local_substitution_replayed"] is True
    assert result["r3r35_public_candidate_preserved"] is True
    assert result["legacy_single_factor_candidate_preserved"] is True
    assert result["shared_dfs_source_order_gate_verified"] is False
    assert result["root_group_proved"] is False
