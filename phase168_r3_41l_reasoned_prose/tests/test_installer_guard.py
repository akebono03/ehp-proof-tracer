"""Standalone checks for the guarded R3-41L installer and complete replacement."""
from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

import pytest


PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("phase168_r3_41l_installer", PACKAGE / "install.py")
INSTALL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALL)


def prior_source() -> bytes:
    return ((PACKAGE / "import_section_full.py").read_bytes()
            + (PACKAGE / "expected_renderer_function_full.py").read_bytes())


def test_verified_original_source_and_only_one_function():
    data = prior_source()
    assert INSTALL.sha256(data) == INSTALL.EXPECTED_SHA256
    replacement = (PACKAGE / "modified_function_full.py").read_text(encoding="utf-8")
    result = INSTALL.patch_function(data, replacement)
    assert result != data
    parsed = ast.parse(result.decode("utf-8"))
    assert [node.name for node in parsed.body if isinstance(node, ast.FunctionDef)] == [
        "render_model_backed_narrative_markdown"
    ]
    assert result.startswith((PACKAGE / "import_section_full.py").read_bytes())


def test_reject_nonfunction_or_wrong_function_name():
    original = prior_source()
    with pytest.raises(RuntimeError, match="exactly one complete renderer function"):
        INSTALL.patch_function(original, "def other_function():\n    return None\n")
    with pytest.raises(RuntimeError, match="exactly one complete renderer function"):
        INSTALL.patch_function(original, "def one():\n    pass\ndef two():\n    pass\n")


def test_isolated_installer_backup_and_exact_restore(tmp_path, monkeypatch):
    target = tmp_path / "phase168_r3_5_model_renderer.py"
    target.write_bytes(prior_source())
    output = tmp_path / "output"
    monkeypatch.setattr(INSTALL, "TARGET", target)
    monkeypatch.setattr(INSTALL, "OUTPUT", output)
    monkeypatch.setattr(INSTALL, "BACKUP", output / "phase168_r3_5_model_renderer.py.before")
    monkeypatch.setattr(INSTALL, "FULL_FILE", output / "phase168_r3_5_model_renderer.py")
    assert INSTALL.main() == 0
    assert target.read_bytes() != prior_source()
    assert INSTALL.BACKUP.read_bytes() == prior_source()
    assert INSTALL.FULL_FILE.read_bytes() == target.read_bytes()
    target.write_bytes(INSTALL.BACKUP.read_bytes())
    assert target.read_bytes() == prior_source()


def test_isolated_installer_fails_closed_on_changed_source(tmp_path, monkeypatch):
    target = tmp_path / "phase168_r3_5_model_renderer.py"
    target.write_bytes(prior_source() + b"\n# unknown edit\n")
    output = tmp_path / "output"
    monkeypatch.setattr(INSTALL, "TARGET", target)
    monkeypatch.setattr(INSTALL, "OUTPUT", output)
    monkeypatch.setattr(INSTALL, "BACKUP", output / "phase168_r3_5_model_renderer.py.before")
    monkeypatch.setattr(INSTALL, "FULL_FILE", output / "phase168_r3_5_model_renderer.py")
    before = target.read_bytes()
    with pytest.raises(RuntimeError, match="nothing patched"):
        INSTALL.main()
    assert target.read_bytes() == before
    assert not output.exists()
