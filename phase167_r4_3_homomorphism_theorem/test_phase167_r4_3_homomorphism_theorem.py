from pathlib import Path

from web_group_proof import build_standard_web_group_proof_view


def _pi43_narrative() -> str:
    view = build_standard_web_group_proof_view(
        3,
        1,
        max_depth=2,
        mode="narrative",
    )
    return "\n".join(view.rendered_lines)


def test_phase167_r4_3_uses_homomorphism_theorem_label_only():
    rendered = _pi43_narrative()

    assert "第一同型定理" not in rendered
    assert "準同型定理" in rendered


def test_phase167_r4_3_preserves_pi43_quotient_argument():
    rendered = _pi43_narrative()

    assert "完全性より" in rendered
    assert r"\operatorname{Im}\Delta" in rendered
    assert r"\ker E" in rendered
    assert "は全射" in rendered
    assert r"\cong" in rendered
    assert r"/\mathbb{Z}\{" in rendered
