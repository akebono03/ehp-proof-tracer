"""Focused structural protection for the model-backed public cutover."""
from __future__ import annotations

import ast
from pathlib import Path
import subprocess

import pytest

from phase173_r4_r12r4_public_tree_cutover import install
from phase173_r4_r12r4_public_tree_cutover.install import (
    replace_function,
)


def test_full_adapter_does_not_use_post_render_narrative_override() -> None:
    fixture = (Path(__file__).resolve().parents[1] / "fixtures"
               / "web_adapter_FULL.py").read_text(encoding="utf-8")
    parsed = ast.parse(fixture)
    matches = tuple(node for node in parsed.body
                    if isinstance(node, ast.FunctionDef)
                    and node.name == "build_partial_web_group_proof_view")
    assert len(matches) == 1
    assert "render_model_backed_narrative_markdown(result, narrative_model)" in fixture
    assert "project_verified_pi74_narrative" not in fixture
    assert "project_verified_toda56_narrative" not in fixture
    assert not any(isinstance(node, ast.Constant) and node.value is Ellipsis
                   for node in ast.walk(parsed))


def test_replacement_requires_full_single_function() -> None:
    source = "def inspect_dimension(value):\n    return value\n"
    full = "def inspect_dimension(value):\n    return value + 1\n"
    assert replace_function(source, "inspect_dimension", full) == full
    with pytest.raises(RuntimeError, match="Full function replacement"):
        replace_function(source, "inspect_dimension", "x = 3\n")


def test_all_patch_fixtures_compile() -> None:
    folder = Path(__file__).resolve().parents[1] / "fixtures"
    for filename in (
        "web_adapter_FULL.py", "inspect_dimension_FULL.py", "test_audit_FULL.py",
    ):
        source = (folder / filename).read_text(encoding="utf-8")
        assert ast.parse(source)


def _git_in_test_repo(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True,
        encoding="utf-8", check=True,
    )
    return completed.stdout.strip()


def _new_reviewed_test_repo(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "repository"
    root.mkdir()
    _git_in_test_repo(root, "init", "-q")
    _git_in_test_repo(root, "config", "user.name", "Audit Test")
    _git_in_test_repo(root, "config", "user.email", "audit@example.invalid")
    (root / "seed.txt").write_text("reviewed baseline\n", encoding="utf-8")
    _git_in_test_repo(root, "add", "seed.txt")
    _git_in_test_repo(root, "commit", "-q", "-m", "reviewed baseline")
    return root, _git_in_test_repo(root, "rev-parse", "HEAD")


def test_reviewed_head_lineage_allows_only_audit_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, base = _new_reviewed_test_repo(tmp_path)
    monkeypatch.setattr(install, "REVIEWED_HEAD", base)
    audit = root / "phase173_r4_r12r3_architecture_audit" / "audit_result.json"
    audit.parent.mkdir(parents=True)
    audit.write_text("{}\n", encoding="utf-8")
    _git_in_test_repo(root, "add", str(audit.relative_to(root)))
    _git_in_test_repo(root, "commit", "-q", "-m", "audit only")
    head = _git_in_test_repo(root, "rev-parse", "HEAD")
    assert install.reviewed_head_lineage_allowed(root, base) is True
    assert install.reviewed_head_lineage_allowed(root, head) is True


def test_reviewed_head_lineage_rejects_production_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, base = _new_reviewed_test_repo(tmp_path)
    monkeypatch.setattr(install, "REVIEWED_HEAD", base)
    production = root / "phase168_r3_5_model_renderer.py"
    production.write_text("# changed renderer\n", encoding="utf-8")
    _git_in_test_repo(root, "add", production.name)
    _git_in_test_repo(root, "commit", "-q", "-m", "unexpected renderer change")
    head = _git_in_test_repo(root, "rev-parse", "HEAD")
    assert install.reviewed_head_lineage_allowed(root, head) is False
