"""Pure common formatting tests; no proof search or inferred evidence."""
from __future__ import annotations

from pathlib import Path

from phase173_r4_r15r14_common_partial_presentation.patches import patch_layout


def load_reviewed_layout_contract():
    """Test the exact proposed layout without modifying production files in DryRun."""
    root = Path(__file__).resolve().parents[2]
    source_file = root / "phase173_r4_r15r13_unified_presentation" / "layout.py"
    source = source_file.read_text(encoding="utf-8")
    if "def _public_search_diagnostic_line" not in source:
        source = patch_layout(source)
    environment = {"__name__": "r15r14_layout_contract_preview"}
    exec(compile(source, str(source_file), "exec"), environment)
    return (environment["canonicalize_proof_layout"],
            environment["_public_search_diagnostic_line"])


canonicalize_proof_layout, _public_search_diagnostic_line = load_reviewed_layout_contract()


def test_registered_derivation_diagnostic_becomes_readable() -> None:
    diagnostic = (
        "expected a verified registered derivation for "
        "Relation(lhs=TodaPrimaryGroup(group_dimension=12, sphere_dimension=4)), found 0"
    )
    assert _public_search_diagnostic_line("- " + diagnostic) == (
        "- 登録済みの前提から証明目標を導く検証済みの推論が見つかりませんでした"
        "（導出候補 0 件）。"
    )


def test_non_diagnostic_text_is_preserved() -> None:
    untouched = "- Relation(lhs=TodaPrimaryGroup(group_dimension=12))"
    assert canonicalize_proof_layout(
        "使用する結果\n\n証明\n\n## 未解決 Goal\n\n" + untouched + "\n"
    ).endswith(untouched + "\n")


def test_public_diagnostics_do_not_affect_goals_or_references() -> None:
    raw = (
        "## 使用する結果\n\n**[R1] Lemma 5.4.**\n\n"
        "---\n\n## 証明\n\n## 未解決 Goal\n\n"
        "- $\\pi_{12}^{4}=\\mathbb{Z}/2\\{\\varepsilon_{4}\\}$\n\n"
        "## 探索診断\n\n"
        "- expected a verified registered derivation for Relation(lhs=some), found 0\n\n"
        "## 証明済みの抽象群構造\n\n$\\pi_{12}^{4}\\cong\\mathbb{Z}/2$.\n"
    )
    shown = canonicalize_proof_layout(raw)
    assert shown.count("[R1]") == 1
    assert r"- $\pi_{12}^{4}=\mathbb{Z}/2\{\varepsilon_{4}\}$" in shown
    assert r"$\pi_{12}^{4}\cong\mathbb{Z}/2$" in shown
    assert "## 探索診断" in shown
    assert "Relation(" not in shown
    assert "導出候補 0 件" in shown


def test_unrecognized_diagnostic_keeps_plain_text() -> None:
    line = "- 証明探索の範囲内に証明規則がありません"
    assert _public_search_diagnostic_line(line) == line


def test_unrecognized_object_repr_is_not_exposed_in_diagnostics() -> None:
    line = "- Relation(lhs=TodaPrimaryGroup(group_dimension=12))"
    shown = _public_search_diagnostic_line(line)
    assert "Relation(" not in shown
    assert "監査ログ" in shown


def test_no_citation_section_is_left_untouched() -> None:
    source = "## 探索診断\n\n- Relation(foo)\n"
    assert canonicalize_proof_layout(source) == source
