"""Minimal fail-closed generic narrative contracts and source patch tests."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r70_verified_narrative_projection.install import (
    BEFORE, AFTER, REVIEWED_BLOB, TARGET, git_blob_sha, replace_formatter,
    source_guard,
)
from phase174_r3_r7_r70_verified_narrative_projection.projection import (
    _body_index, _step_index, project_verified_general_narrative,
)


def test_patch_updates_only_entire_formatter_and_is_idempotent() -> None:
    root = Path(__file__).resolve().parents[2]
    assert source_guard(root)
    raw = (root / TARGET).read_bytes()
    state, rewritten = replace_formatter(raw)
    assert state == "ALREADY_APPLIED"
    assert rewritten == raw
    assert BEFORE.encode() not in rewritten
    assert AFTER.encode() in rewritten.replace(b"\r\n", b"\n")


def test_line_endings_source_guard_and_patch_idempotence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import phase174_r3_r7_r70_verified_narrative_projection.install as module
    sample = b"# test only\n" + BEFORE.encode("utf-8")
    monkeypatch.setattr(module, "REVIEWED_BLOB", git_blob_sha(sample))
    for content in (sample, sample.replace(b"\n", b"\r\n")):
        state, patched = module.replace_formatter(content)
        assert state == "PATCH_REQUIRED"
        assert b"\r\r\n" not in patched
        assert module.replace_formatter(patched) == ("ALREADY_APPLIED", patched)


def test_source_guard_rejects_unreviewed_change(monkeypatch: pytest.MonkeyPatch) -> None:
    import phase174_r3_r7_r70_verified_narrative_projection.install as module
    monkeypatch.setattr(module, "REVIEWED_BLOB", git_blob_sha(BEFORE.encode()))
    with pytest.raises(RuntimeError, match="R70_SOURCE_GUARD_FAILED"):
        module.replace_formatter(("# extra\n" + BEFORE).encode())


def test_rejects_mixed_eol_and_cr_only() -> None:
    import phase174_r3_r7_r70_verified_narrative_projection.install as module
    with pytest.raises(RuntimeError, match="R70_UNEXPECTED_CR"):
        module.replace_formatter(b"a\rb\n")
    with pytest.raises(RuntimeError, match="R70_MIXED_EOL"):
        module.replace_formatter(b"a\r\nb\n")


def test_body_line_search_does_not_match_reference_text() -> None:
    lines = ["使用する結果", "[R1]より, $x=0$.", "証明", "", "[R1]より, $x=0$."]
    assert _body_index(lines, "$x=0$.", prefix="[R1]より, ") == 4
    assert _body_index(lines, "$x=0$.", prefix="[R2]より, ") is None
    assert _body_index(["証明", "$x=0$.", "$x=0$."], "$x=0$.") is None


def test_step_index_rejects_ambiguous_value_fallback() -> None:
    source = SimpleNamespace(conclusion="x", premises=())
    identical = SimpleNamespace(conclusion="x", premises=())
    model = SimpleNamespace(steps=(source, identical))
    assert _step_index(model, source, frozenset({0, 1})) == 0
    assert _step_index(model, SimpleNamespace(conclusion="x", premises=()),
                       frozenset({0, 1})) is None


def test_incomplete_model_has_no_composed_rewrite() -> None:
    original = ["証明", "", "未完成", ""]
    model = SimpleNamespace(root_index=None)
    assert project_verified_general_narrative(original, model) == original


def test_git_sha_fixture() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
