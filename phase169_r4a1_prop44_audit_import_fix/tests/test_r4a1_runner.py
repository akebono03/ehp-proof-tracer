"""R4A1 regression: audit must run as a module from the repository root."""
from __future__ import annotations

from pathlib import Path


def test_r4a1_launcher_uses_repo_relative_module_execution():
    package_dir = Path(__file__).resolve().parents[1]
    source = (package_dir / "run.ps1").read_text(encoding="utf-8")
    assert "$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path" in source
    assert "Push-Location $root" in source
    assert "python -m phase169_r4a1_prop44_audit_import_fix.audit" in source
    assert "python (Join-Path $PSScriptRoot 'audit.py')" not in source
    assert (package_dir / "audit.py").is_file()
    assert (package_dir / "__init__.py").is_file()
