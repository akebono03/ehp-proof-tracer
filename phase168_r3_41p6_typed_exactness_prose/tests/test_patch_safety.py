"""Self-contained package and safe patch unit tests (no project imports)."""
from __future__ import annotations
import ast
from pathlib import Path
import pytest
from phase168_r3_41p6_typed_exactness_prose.patch import (
    OLD_BLOCK, NEW_BLOCK, full_function, transform, sha256,
)


def _sample():
    return (
        "from __future__ import annotations\n"
        "def typed_sentence(statement, step):\n"
        "    if True:\n"
        + OLD_BLOCK
        + "                        return 1\n"
        + "    return None\n"
    )


def test_single_function_replacement_preserves_other_content():
    source = _sample()
    changed = transform(source)
    assert OLD_BLOCK not in changed
    assert changed.count(NEW_BLOCK) == 1
    assert full_function(changed).startswith("def typed_sentence(")
    assert 'from __future__ import annotations' in changed
    ast.parse(changed)


def test_missing_or_duplicate_pattern_refuses_changes():
    with pytest.raises(ValueError):
        transform(_sample().replace(OLD_BLOCK, ""))
    with pytest.raises(ValueError):
        transform(_sample().replace(OLD_BLOCK, OLD_BLOCK + OLD_BLOCK))


def test_only_function_is_modified():
    original = _sample() + "\ndef untouched():\n    return 'sentinel'\n"
    changed = transform(original)
    assert "def untouched():\n    return 'sentinel'" in changed
    assert changed.endswith("def untouched():\n    return 'sentinel'\n")


def test_sha256_known_value():
    assert sha256(b"abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_apply_and_restore_isolated_file_preserves_bytes_and_outputs(tmp_path, monkeypatch):
    import phase168_r3_41p6_typed_exactness_prose.patch as patch_module
    import phase168_r3_41p6_typed_exactness_prose.restore as restore_module

    package = Path(__file__).resolve().parents[1]
    new_function = (package / "typed_sentence_FULL.py").read_text(encoding="utf-8")
    old_function = new_function.replace(NEW_BLOCK, OLD_BLOCK, 1)
    original = (
        "from __future__ import annotations\n\n"
        + old_function
        + "\ndef unrelated_function():\n    return 7\n"
    )
    initial_bytes = original.replace("\n", "\r\n").encode("utf-8")
    target = tmp_path / "phase168_r3_27_typed_statement_projection.py"
    target.write_bytes(initial_bytes)
    output = tmp_path / "out"
    backup = output / "backups" / target.name
    monkeypatch.setattr(patch_module, "TARGET", target)
    monkeypatch.setattr(patch_module, "OUTPUT", output)
    monkeypatch.setattr(patch_module, "BACKUP", backup)
    monkeypatch.setattr(patch_module, "EXPECTED_SHA256", sha256(initial_bytes))
    monkeypatch.setattr(restore_module, "TARGET", target)
    monkeypatch.setattr(restore_module, "OUTPUT", output)
    monkeypatch.setattr(restore_module, "BACKUP", backup)
    patch_module.apply()
    changed = target.read_bytes().decode("utf-8")
    assert "\r\n" in changed
    assert changed.replace("\r\n", "\n").count(NEW_BLOCK) == 1
    assert "def unrelated_function():\r\n    return 7" in changed
    assert backup.read_bytes() == initial_bytes
    assert (output / "typed_sentence_FULL.py").read_text(encoding="utf-8") == new_function
    restore_module.restore()
    assert target.read_bytes() == initial_bytes
