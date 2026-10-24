"""Standalone tests for safe single-function replacement."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase168_r3_41p5_rule_name_independent import patch


def sample_source() -> str:
    return (
        "def render_model_backed_narrative_markdown():\n"
        + patch.OLD_RULE_IMPORT
        + "    if not incomplete:\n"
        + patch.OLD_IMPORT
        + "        if (True\n"
        + patch.OLD_CONDITION
        + "                        and transported.lhs == witness_step.conclusion.map.target_group):\n"
        + "            pass\n"
    )


def test_transform_preserves_the_complete_renderer_function():
    source = sample_source()
    updated = patch.transform(source)
    assert patch.OLD_CONDITION not in updated
    assert patch.NEW_CONDITION in updated
    assert patch.NEW_IMPORT in updated
    assert "def render_model_backed_narrative_markdown" in patch.extract_full_function(updated)
    ast.parse(updated)


def test_refuses_unknown_or_already_patched_condition():
    source = sample_source()
    with pytest.raises(ValueError, match="not found exactly once"):
        patch.transform(source.replace(patch.OLD_CONDITION, ""))
    with pytest.raises(ValueError, match="not found exactly once"):
        patch.transform(patch.transform(source))


def test_exactly_one_import_and_one_condition_are_required():
    source = sample_source()
    with pytest.raises(ValueError, match="local import"):
        patch.transform(source.replace(patch.OLD_IMPORT, "", 1))
    with pytest.raises(ValueError, match="not found exactly once"):
        patch.transform(source.replace(patch.OLD_CONDITION, patch.OLD_CONDITION * 2))


def test_digest_distinguishes_line_endings():
    source = sample_source()
    assert patch.digest(source.encode("utf-8")) != patch.digest(
        source.replace("\n", "\r\n").encode("utf-8")
    )

@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_apply_and_restore_keep_original_line_endings(tmp_path, monkeypatch, newline):
    from phase168_r3_41p5_rule_name_independent import restore

    target = tmp_path / "phase168_r3_5_model_renderer.py"
    original = sample_source().replace("\n", newline).encode("utf-8")
    target.write_bytes(original)
    output = tmp_path / "package_output"
    backup = output / "backups" / target.name
    original_sha = patch.digest(original)
    for module in (patch, restore):
        monkeypatch.setattr(module, "TARGET", target)
        monkeypatch.setattr(module, "OUTPUT", output)
        monkeypatch.setattr(module, "BACKUP", backup)
        monkeypatch.setattr(module, "EXPECTED_SHA256", original_sha)
    patch.apply()
    altered = target.read_bytes()
    assert altered != original
    assert backup.read_bytes() == original
    assert (output / "render_model_backed_narrative_markdown_FULL.py").is_file()
    if newline == "\r\n":
        assert b"\r\n" in altered
        assert altered.count(b"\n") == altered.count(b"\r\n")
    restore.restore()
    assert target.read_bytes() == original
