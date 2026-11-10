"""R54 read-only scope, source pinning, and no skipped implementation."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r54_sources_parse_and_have_no_ellipsis() -> None:
    sources = tuple(PACKAGE.glob("*.py")) + tuple((PACKAGE / "tests").glob("test_*.py"))
    assert len(sources) >= 6
    for path in sources:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        assert not any(isinstance(node, ast.Constant) and node.value is Ellipsis
                       for node in ast.walk(tree)), path


def test_run_script_is_read_only_and_focused() -> None:
    source = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "--dry-run" in source
    assert "-p no:cacheprovider" in source
    assert "--import-mode=importlib" in source
    assert "FULL_PYTEST=False" in source
    for unwanted in ("git reset", "git clean", "git add", "git commit", "install.py"):
        assert unwanted not in source


def test_audit_uses_real_flask_and_no_proof_injection() -> None:
    source = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert "from web_app import create_app" in source
    assert 'client.post("/", data=payload)' in source
    assert "form_kind" in source
    assert '"group_proof"' in source
    assert '"group"' in source
    assert "ProofStep(" not in source
    assert "monkeypatch.setattr(" not in source
    assert "patch.object" not in source
    assert '"browser_katex_checked": False' in source
