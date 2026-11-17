"""Pinned whole-function installation contracts."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r4r5r3_public_order_zero import installer


SOURCE = '''from collections import namedtuple


def shared_expansion_provider(bridge, prior_conclusions=()):
    value = (1,)
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")
    return value


def unaffected():
    return "unchanged"
'''


def test_whole_function_replacement_is_exact_and_has_no_other_changes() -> None:
    changed, whole = installer.function_replacement(SOURCE)
    assert changed.count("build_public_order_zero_provider") == 2
    assert "return value" in whole
    assert ast.parse(changed)
    assert changed.split("\ndef unaffected()", 1)[1] == SOURCE.split("\ndef unaffected()", 1)[1]
    assert changed[:changed.index("def shared_expansion_provider")] == SOURCE[:SOURCE.index("def shared_expansion_provider")]
    assert installer.INSERTION.strip() in whole


@pytest.mark.parametrize("invalid", [
    SOURCE.replace("if not isinstance(prior_conclusions, tuple):", "if prior_conclusions is None:"),
    SOURCE.replace("def shared_expansion_provider", "def another_provider"),
    SOURCE + SOURCE,
])
def test_fail_closed_for_changed_function_or_duplicate(invalid: str) -> None:
    with pytest.raises(RuntimeError):
        installer.function_replacement(invalid)


def test_source_pin_guard_rejects_modified_original(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / installer.TARGET_RELATIVE
    path.write_text(SOURCE, encoding="utf-8")
    monkeypatch.setattr(installer, "git_blob", lambda root, ref: "unreviewed")
    with pytest.raises(RuntimeError, match="PRODUCTION_SOURCE_BLOB_CHANGED"):
        installer.plan(tmp_path)


def test_plan_never_fabricates_a_goal() -> None:
    assert "eta_7" not in installer.INSERTION
    assert "pi_9^5" not in installer.INSERTION
    assert "GIVEN" not in installer.INSERTION


def test_full_install_replaces_only_function_in_temporary_git_repo(
    tmp_path: Path, monkeypatch,
) -> None:
    import subprocess

    target = tmp_path / installer.TARGET_RELATIVE
    target.write_text(SOURCE, encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", installer.TARGET_RELATIVE.as_posix()],
                   cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com",
                    "commit", "-qm", "synthetic fixture"], cwd=tmp_path, check=True)
    synthetic_blob = installer.git_blob(
        tmp_path, "HEAD:" + installer.TARGET_RELATIVE.as_posix(),
    )
    monkeypatch.setattr(installer, "PINNED_GIT_BLOB", synthetic_blob)
    output = tmp_path / "audit-output"
    dry = installer.install(tmp_path, dry_run=True, output=output)
    assert target.read_text(encoding="utf-8") == SOURCE
    assert Path(dry["full_replacement_path"]).is_file()
    installed = installer.install(tmp_path, dry_run=False, output=output)
    assert installed["dry_run"] is False
    changed = target.read_text(encoding="utf-8")
    assert "build_public_order_zero_provider" in changed
    assert changed.split("def unaffected():", 1)[1] == SOURCE.split("def unaffected():", 1)[1]
    assert "build_public_order_zero_provider" in Path(
        installed["full_replacement_path"],
    ).read_text(encoding="utf-8")
