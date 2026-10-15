"""Check that last top-level renderer definition is patched, including shadowing."""
from __future__ import annotations

import ast
from pathlib import Path

from install import effective_function_source, function_nodes, install


def _project(tmp_path: Path) -> Path:
    target = tmp_path / "toda_group_proof_generic_narrative_renderer.py"
    target.write_text(
        "def render_toda_partial_proof_narrative_markdown(result):\n"
        "    target = statement_math(result.open_goals[0])\n"
        "    return target\n\n"
        "def render_toda_partial_proof_narrative_markdown(result):\n"
        "    target = statement_math(result.open_goals[0])\n"
        "    return target\n", encoding="utf8"
    )
    return target


def test_r21_r1_patches_effective_last_definition(tmp_path: Path):
    target = _project(tmp_path)
    package = Path(__file__).resolve().parent
    assert install(tmp_path, package) == "INSTALLED"
    source = target.read_text(encoding="utf8")
    assert len(function_nodes(source)) == 2
    assert "candidate_goals" in effective_function_source(source)
    assert "## 使用する結果" in effective_function_source(source)


def test_r21_r1_idempotent(tmp_path: Path):
    target = _project(tmp_path)
    package = Path(__file__).resolve().parent
    assert install(tmp_path, package) == "INSTALLED"
    before = target.read_bytes()
    assert install(tmp_path, package) == "ALREADY_INSTALLED"
    assert target.read_bytes() == before


def test_r21_r1_rejects_unknown_renderer(tmp_path: Path):
    import pytest
    target = tmp_path / "toda_group_proof_generic_narrative_renderer.py"
    target.write_text("def render_toda_partial_proof_narrative_markdown(result):\n    return 'unknown'\n", encoding="utf8")
    with pytest.raises(RuntimeError, match="unrecognized"):
        install(tmp_path, Path(__file__).resolve().parent)


def test_r21_r1_loaded_source_matches_runtime():
    import inspect
    import toda_group_proof_generic_narrative_renderer as renderer
    code = inspect.getsource(renderer.render_toda_partial_proof_narrative_markdown)
    assert "candidate_goals" in code
    assert "## 使用する結果" in code
    assert "## 証明" in code
