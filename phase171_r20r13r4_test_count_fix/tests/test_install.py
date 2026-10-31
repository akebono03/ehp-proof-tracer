"""Guarded repair checks: a list contains lines, not substrings."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase171_r20r13r4_test_count_fix import install


def test_exact_reviewed_single_assertion_replacement():
    source = install.normalized(
        (install.HERE / "reviewed_test.py").read_bytes()
    )
    assert install.sha256(source) in (
        install.ORIGINAL_SHA256, install.CORRECTED_SHA256,
    )
    fixed = source.replace(install.OLD, install.NEW)
    assert install.sha256(fixed) == install.CORRECTED_SHA256
    assert "sum(line.startswith" in fixed
    assert "actual.count(" not in fixed


def test_count_validates_prefixed_lines_not_a_separate_list_member():
    actual = ["証明", "", r"[R3]より, $E(\\eta_{2})=\\eta_{3},\\quad E(\\eta_{3}^{2})=\\eta_{4}^{2}$.", "□"]
    assert actual.count("[R3]より, ") == 0
    assert sum(line.startswith("[R3]より, ") for line in actual) == 1


def test_unknown_test_content_is_rejected(monkeypatch, tmp_path):
    target = tmp_path / install.TARGET
    target.parent.mkdir(parents=True)
    target.write_bytes(b"unreviewed test")
    projection = tmp_path / install.PROJECTION
    projection.parent.mkdir(parents=True)
    projection.write_text("untrusted projection", encoding="utf-8")
    monkeypatch.setattr(install, "PROJECTION_SHA256", install.sha256("untrusted projection"))
    renderer = tmp_path / install.RENDERER
    renderer.parent.mkdir(parents=True, exist_ok=True)
    renderer.write_text("format_complete_proof_sentences(lines, model)", encoding="utf-8")
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "git", lambda *args: "develop" if args[0] == "branch" else "any-head")
    with pytest.raises(RuntimeError, match="differs from reviewed"):
        install.preflight()
    assert target.read_bytes() == b"unreviewed test"


def test_reviewed_original_test_can_be_patched(monkeypatch, tmp_path):
    reviewed = (install.HERE / "reviewed_test.py").read_bytes()
    target = tmp_path / install.TARGET
    target.parent.mkdir(parents=True)
    target.write_bytes(reviewed)
    projection = tmp_path / install.PROJECTION
    projection.parent.mkdir(parents=True)
    projection.write_text("reviewed synthetic projection", encoding="utf-8")
    renderer = tmp_path / install.RENDERER
    renderer.parent.mkdir(parents=True, exist_ok=True)
    renderer.write_text("format_complete_proof_sentences(lines, model)", encoding="utf-8")
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "PROJECTION_SHA256", install.sha256("reviewed synthetic projection"))
    monkeypatch.setattr(install, "git", lambda *args: "develop" if args[0] == "branch" else "new HEAD")
    head, before, after, already = install.preflight()
    assert head == "new HEAD"
    assert before == reviewed
    assert already is False
    assert install.sha256(install.normalized(after)) == install.CORRECTED_SHA256
    assert target.read_bytes() == reviewed


def test_corrected_test_is_idempotent(monkeypatch, tmp_path):
    reviewed = (install.HERE / "reviewed_test.py").read_text(encoding="utf-8")
    corrected = reviewed.replace(install.OLD, install.NEW, 1).encode("utf-8")
    target = tmp_path / install.TARGET
    target.parent.mkdir(parents=True)
    target.write_bytes(corrected)
    projection = tmp_path / install.PROJECTION
    projection.parent.mkdir(parents=True)
    projection.write_text("reviewed synthetic projection", encoding="utf-8")
    renderer = tmp_path / install.RENDERER
    renderer.parent.mkdir(parents=True, exist_ok=True)
    renderer.write_text("format_complete_proof_sentences(lines, model)", encoding="utf-8")
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "PROJECTION_SHA256", install.sha256("reviewed synthetic projection"))
    monkeypatch.setattr(install, "git", lambda *args: "develop" if args[0] == "branch" else "new HEAD")
    head, before, after, already = install.preflight()
    assert already is True
    assert before == after == corrected
