"""R3-41P2 launcher and single-test expectation replacement tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase168_r3_41p_boundary_audit.apply_test_fix import (
    NEW, OLD, TARGET, apply_legacy_test_fix,
)
from phase168_r3_41p_boundary_audit.restore_test import restore_legacy_test


def sample_test_file(project: Path, newline: str) -> bytes:
    path = project / TARGET
    path.parent.mkdir(parents=True)
    code = (
        "def test_another_case():\n"
        "    assert 2 + 2 == 4\n\n"
        "def test_pi32_all_steps_preserved_without_suppression():\n"
        "    rendered = 'dummy'\n"
        + OLD + "\n"
        "    assert rendered.count('次の完全列を考える') == 1\n"
    ).replace("\n", newline)
    path.write_bytes(code.encode("utf-8"))
    return path.read_bytes()


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_one_test_expectation_is_patched_and_restorable(tmp_path, newline):
    project = tmp_path / "project"
    original = sample_test_file(project, newline)
    backups = tmp_path / "backups"
    result = apply_legacy_test_fix(project, backups)
    assert result["status"] == "patched"
    changed = (project / TARGET).read_bytes()
    assert changed == original.replace(OLD.encode("utf-8"), NEW.encode("utf-8"), 1)
    assert (backups / "r3_29_test_original.bin").read_bytes() == original
    assert apply_legacy_test_fix(project, backups)["status"] == "already_patched"
    assert restore_legacy_test(project, backups)["status"] == "restored"
    assert (project / TARGET).read_bytes() == original


def test_unknown_test_expectation_is_never_modified(tmp_path):
    project = tmp_path / "project"
    sample_test_file(project, "\n")
    path = project / TARGET
    path.write_bytes(path.read_bytes().replace(OLD.encode(), b"    assert False"))
    before = path.read_bytes()
    with pytest.raises(ValueError, match="refusing to patch"):
        apply_legacy_test_fix(project, tmp_path / "backups")
    assert path.read_bytes() == before


def test_restore_refuses_to_overwrite_later_user_edit(tmp_path):
    project = tmp_path / "project"
    sample_test_file(project, "\n")
    backups = tmp_path / "backups"
    apply_legacy_test_fix(project, backups)
    path = project / TARGET
    changed = path.read_bytes() + b"\n# user edit\n"
    path.write_bytes(changed)
    with pytest.raises(ValueError, match="later edits"):
        restore_legacy_test(project, backups)
    assert path.read_bytes() == changed


def test_launcher_uses_module_context_for_sibling_imports():
    runner = Path(__file__).resolve().parents[1] / "run.ps1"
    script = runner.read_text(encoding="utf-8-sig")
    assert '-PythonArguments @("-B", "-m", "phase168_r3_41p_boundary_audit.audit")' in script
    assert '-WorkingDirectory $project' in script
    assert 'phase168_r3_41p_boundary_audit.apply_test_fix' in script
    assert 'FULL_PYTEST_NOT_RUN' in script
