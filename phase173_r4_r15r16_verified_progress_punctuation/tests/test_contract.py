"""Tests of R15R16 shared prose layout and pure patch invariants."""
from __future__ import annotations

import pytest

from phase173_r4_r15r13_unified_presentation.layout import (
    _normalize_narrative_punctuation,
    canonicalize_proof_layout,
)
from phase173_r4_r15r16_verified_progress_punctuation.projection_patch import (
    patch_layout,
    patch_projection,
    PROJECTION_OLD,
    LAYOUT_OLD,
)


def test_actual_prose_periods_are_line_breaks() -> None:
    markdown = (
        "使用する結果\n\n**[R1] Proposition 4.4.**\n\n"
        "証明\n\nこれは確認済みである。続いて、定理を使う.次の結論を得た.\n"
    )
    converted = canonicalize_proof_layout(markdown)
    assert "## 使用する結果" in converted
    assert "Proposition 4.4." in converted
    assert "これは確認済みである.\n続いて, 定理を使う.\n次の結論を得た." in converted
    assert converted.count("\n---\n") == 1


def test_math_code_and_numbered_source_are_not_changed() -> None:
    converted = _normalize_narrative_punctuation([
        r"$H(\nu_4)=\iota_7$ と $\pi_{12}^4$ を示す。次へ進む.",
        "**[R1] Proposition 4.4.**",
        r"\[",
        r"\pi_{12}^{4}=\mathbb{Z}/2",
        r"\]",
        "`x.3` を用い、0.5 の関係を確認した。",
    ])
    assert converted[0] == r"$H(\nu_4)=\iota_7$ と $\pi_{12}^4$ を示す."
    assert converted[1] == "次へ進む."
    assert "**[R1] Proposition 4.4.**" in converted
    assert r"\pi_{12}^{4}=\mathbb{Z}/2" in converted
    assert "`x.3` を用い, 0.5 の関係を確認した." in converted


def test_no_status_or_group_names_required_for_punctuation() -> None:
    first = canonicalize_proof_layout("使用する結果\n\n証明\n\n結果である。結論を示す。\n")
    second = canonicalize_proof_layout("使用する結果\n\n証明\n\n検証した。未解決である。\n")
    assert "結果である.\n結論を示す." in first
    assert "検証した.\n未解決である." in second


def test_source_mismatch_is_rejected() -> None:
    with pytest.raises(RuntimeError, match="reviewed function boundary mismatch"):
        patch_projection("unrelated source")
    with pytest.raises(RuntimeError, match="reviewed function boundary mismatch"):
        patch_layout("unrelated source")
    assert patch_projection(PROJECTION_OLD).count("## 検証済みの途中経過") == 1
    assert "_normalize_narrative_punctuation(normalized)" in patch_layout(LAYOUT_OLD)
