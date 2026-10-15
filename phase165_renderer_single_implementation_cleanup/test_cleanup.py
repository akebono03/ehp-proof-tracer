"""Focused single-renderer regression tests."""
from __future__ import annotations

import ast
from pathlib import Path

from phase165_r52_partial_proof import render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r56_presentation_adapter import render_completed_shared_narrative

ROOT = Path(__file__).resolve().parent.parent


def test_duplicate_renderer_file_deleted():
    assert not (ROOT / "toda_group_proof_generic_narrative_renderer.py").exists()
    assert (ROOT / "toda_group_proof_generic_narrative_renderer" / "__init__.py").is_file()


def test_original_narrative_rendering_preserved():
    result = search_group_from_registered_goal(n=2, k=1)
    actual = render_completed_shared_narrative(result)
    assert "## 証明対象" in actual
    assert "## 使用する結果" in actual
    assert "## 証明" in actual
    assert "完全性より" in actual
    assert "以上より" in actual
    assert actual.strip().endswith("□")


def test_both_public_entries_use_single_primary_renderer():
    import inspect
    from toda_group_proof_narrative_renderer import (
        render_toda_partial_proof_narrative_markdown,
    )
    import toda_group_proof_generic_narrative_renderer as alias
    assert alias.render_toda_partial_proof_narrative_markdown is render_toda_partial_proof_narrative_markdown
    source = inspect.getsource(render_partial_proof_markdown)
    assert "from toda_group_proof_narrative_renderer import" in source


def test_partial_result_does_not_become_completed():
    result = search_group_from_registered_goal(n=3, k=1)
    markdown = render_partial_proof_markdown(result)
    assert "## 証明対象" in markdown
    assert "## 使用する結果" in markdown
    assert "## 証明" in markdown
    assert "未解決 Goal" in markdown
    assert "以上より" not in markdown


def test_shared_components_have_no_public_render_functions():
    path = ROOT / "toda_group_proof_narrative_shared_components.py"
    source = path.read_text(encoding="utf8")
    names = {node.name for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)}
    assert "render_toda_partial_proof_narrative_markdown" not in names
    assert "render_toda_group_proof_generic_narrative_markdown" not in names
