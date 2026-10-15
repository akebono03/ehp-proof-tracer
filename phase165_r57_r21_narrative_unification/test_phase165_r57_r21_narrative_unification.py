"""R57-R21: completed and incomplete search share one evidence-based Narrative."""
from __future__ import annotations

from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r56_presentation_adapter import render_completed_shared_narrative


def _root():
    return Path(__file__).resolve().parent.parent


def test_r21_completed_and_partial_public_paths_share_one_renderer():
    completed = search_group_from_registered_goal(n=2, k=1)
    assert completed.status is ProofSearchStatus.COMPLETE
    assert render_completed_shared_narrative(completed) == render_partial_proof_markdown(completed)


def test_r21_completed_has_single_common_sections_and_only_proved_final():
    completed = search_group_from_registered_goal(n=2, k=1)
    markdown = render_partial_proof_markdown(completed)
    assert markdown.count("## 証明対象") == 1
    assert markdown.count("## 使用する結果") == 1
    assert markdown.count("## 証明\n") == 1
    assert markdown.count("以上より") == 1
    assert markdown.endswith("□")
    assert "未解決 Goal" not in markdown
    assert "(5.1)" in markdown


def test_r21_partial_target_remains_original_group_goal():
    partial = search_group_from_registered_goal(n=3, k=1)
    assert partial.status is not ProofSearchStatus.COMPLETE
    rendered = render_partial_proof_markdown(partial)
    heading = rendered.split("## 証明対象", 1)[1].split("## 使用する結果", 1)[0]
    assert "\\pi_{4}^{3}" in heading or "π43" in heading or "π_4^3" in heading
    assert "\\pi_{5}^{5}" not in heading
    assert "未解決 Goal" in rendered
    assert "□" not in rendered


def test_r21_partial_and_completed_share_section_order():
    for n in (2, 3):
        text = render_partial_proof_markdown(search_group_from_registered_goal(n=n, k=1))
        assert text.index("## 証明対象") < text.index("## 使用する結果") < text.index("## 証明\n")


def test_r21_completed_entry_has_no_legacy_replay_or_legacy_renderer():
    code = (_root() / "phase165_r56_presentation_adapter.py").read_text(encoding="utf8")
    assert "build_complete_toda_group_result_proof_replay" not in code
    assert "render_toda_group_proof_narrative_markdown" not in code
    assert "render_toda_partial_proof_narrative_markdown" in code


def test_r21_unchanged_mathematics_and_no_group_specific_renderer_branches():
    code = (_root() / "phase165_r56_presentation_adapter.py").read_text(encoding="utf8")
    assert "n == 2" not in code
    assert "n == 3" not in code
    assert "ProofStep(" not in code
    assert "ProofRule.GIVEN" not in code
