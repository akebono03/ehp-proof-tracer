"""Pure, status-independent presentation contract tests."""
from __future__ import annotations

from phase173_r4_r15r13_unified_presentation.layout import canonicalize_proof_layout


def test_complete_and_partial_share_one_structure() -> None:
    completed = (
        "使用する結果\n\n**[R1] Proposition 4.4.**\n\n"
        "証明\n\n[R1]を用いて, $\\pi_7^4=\\mathbb{Z}$.\n□\n"
    )
    partial = (
        "## 証明対象\n\n$\\pi_{12}^{4}$\n\n"
        "## 使用する結果\n\n参照情報を持つ ProofStep はありません。\n"
        "---\n\n## 証明\n\n**探索状態：証明未完成**\n"
        "## 未解決 Goal\n\n- $\\pi_{12}^{4}$\n"
    )
    full = canonicalize_proof_layout(completed)
    pending = canonicalize_proof_layout(partial)
    for text in (full, pending):
        assert text.count("## 使用する結果") == 1
        assert "\n証明\n" not in text
        assert "## 証明\n" not in text
        assert text.count("\n---\n") == 1
    assert "**[R1] Proposition 4.4.**" in full
    assert "[R1]を用いて" in full and "□" in full
    assert "**探索状態：証明未完成**" in pending
    assert "## 未解決 Goal" in pending
    assert "## 証明対象" not in pending
    assert r"$\pi_{12}^{4}$" in pending


def test_layout_does_not_infer_or_remove_citations() -> None:
    source = (
        "## 使用する結果\n\n**[R1] Lemma 5.4.**\n\n"
        "$H(\\nu_4)=\\iota_7$.\n\n---\n\n## 証明\n\n"
        "**探索状態：証明未完成**\n\n"
        "## 未解決 Goal\n\n- CyclicStructureStatement（数式表示未対応）\n"
    )
    changed = canonicalize_proof_layout(source)
    assert changed.count("[R1]") == source.count("[R1]")
    assert changed.count(r"$H(\nu_4)=\iota_7$") == 1
    assert changed.count("## 未解決 Goal") == 1
    assert "CyclicStructureStatement（数式表示未対応）" in changed
    assert changed.count("\n---\n") == 1


def test_other_text_is_not_changed() -> None:
    source = "## 未解決 Goal\n\n証明\n"
    assert canonicalize_proof_layout(source) == source


def test_type_guard() -> None:
    try:
        canonicalize_proof_layout(None)
    except TypeError:
        pass
    else:
        raise AssertionError("type guard missing")
