"""R57-R10 proof fidelity retained under the strict R57-R11 root order gate."""
from __future__ import annotations

from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r10_step_narrative import has_transport_proof_ancestry


def test_r10_unordered_pi54_specialization_not_claimed_as_proved():
    result = search_group_from_registered_goal(n=4, k=1)
    assert result.status is not ProofSearchStatus.COMPLETE
    assert result.conclusion is None
    assert result.open_goals
    assert not any(has_transport_proof_ancestry(s) for s in result.proven_steps)


def test_r10_incomplete_proof_must_not_gain_conclusion_in_renderer():
    from phase165_r52_partial_proof import render_partial_proof_markdown
    text = render_partial_proof_markdown(search_group_from_registered_goal(n=4, k=1))
    assert "証明" in text
    assert "未解決" in text or "未完成" in text
    assert "[R1]を " not in text
    assert "以上より" not in text


def test_r10_existing_pi32_narrative_is_preserved():
    from phase165_r52_partial_proof import render_partial_proof_markdown
    text = render_partial_proof_markdown(search_group_from_registered_goal(n=2, k=1))
    assert "使用する結果" in text
    assert "証明" in text
    assert "□" in text


def test_r10_adapter_does_not_remove_legacy_renderer():
    text = Path(__file__).resolve().parent.parent.joinpath("toda_group_proof_narrative_renderer.py").read_text(encoding="utf-8")
    assert "_phase160_r7_render_stable_finite_cyclic_transport_narrative" in text
