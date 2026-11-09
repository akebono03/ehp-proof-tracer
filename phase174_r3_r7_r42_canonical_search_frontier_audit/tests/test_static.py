"""R42 is purely observational and does not modify the public proof engine."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_new_python_sources_parse_without_ellipsis():
    for name in ("audit.py", "source_guard.py"):
        parsed = ast.parse((ROOT / name).read_text(encoding="utf-8"))
        assert not any(
            isinstance(node, ast.Constant) and node.value is Ellipsis
            for node in ast.walk(parsed)
        )


def test_no_implementation_installer_or_provider_override():
    assert not (ROOT / "install.py").exists()
    assert not (ROOT / "provider.py").exists()
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    assert "search_registered_partial_proof(" in source
    assert "scoped_probe_not_full_web_search" in source


def test_r42_audit_keeps_proof_completion_false():
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    assert '"root_complete": False' in source
    assert '"web_http_checked": False' in source
    assert '"new_given_statements": 0' in source


def test_powershell_supports_dryrun_and_focused_tests():
    script = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in script
    assert "--dry-run" in script
    assert "pytest -q --import-mode=importlib" in script
    assert "FULL_PYTEST=False" in script
