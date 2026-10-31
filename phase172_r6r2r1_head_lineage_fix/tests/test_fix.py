"""Focused tests for the corrected commit-lineage and source gates."""
from __future__ import annotations

from subprocess import CompletedProcess

import pytest

from phase172_r6r2r1_head_lineage_fix.fix import (
    CORRECTED_SHA256,
    ORIGINAL_SHA256,
    PAYLOAD,
    candidate_module,
    digest,
)


def prepared(monkeypatch):
    module = candidate_module()
    changes = "\n".join("A\t" + path for path in module.ALLOWED_R6_AUDIT_BLOBS)
    observed = []

    def fake_command(*args, **kwargs):
        observed.append(args)
        return CompletedProcess(args, 0, stdout="", stderr="")

    def fake_checked(*args):
        observed.append(args)
        if args[:3] == ("git", "diff", "--name-status"):
            return changes
        if args[:2] == ("git", "rev-parse"):
            path = args[-1][5:]
            return module.ALLOWED_R6_AUDIT_BLOBS[path]
        raise AssertionError("unexpected Git command: " + repr(args))

    monkeypatch.setattr(module, "command", fake_command)
    monkeypatch.setattr(module, "checked", fake_checked)
    return module, observed


def test_original_verified_r6_commit_requires_no_descendant_diff(monkeypatch):
    module, calls = prepared(monkeypatch)
    assert module.reviewed_head_lineage(module.REVIEWED_HEAD) == ()
    assert calls == []


def test_one_reviewed_r6_audit_commit_is_allowed(monkeypatch):
    module, calls = prepared(monkeypatch)
    accepted = module.reviewed_head_lineage("later-reviewed-commit")
    assert set(accepted) == set(module.ALLOWED_R6_AUDIT_BLOBS)
    assert ("git", "merge-base", "--is-ancestor", module.REVIEWED_HEAD,
            "later-reviewed-commit") in calls


def test_non_descendant_commit_is_rejected(monkeypatch):
    module, _ = prepared(monkeypatch)
    monkeypatch.setattr(
        module, "command",
        lambda *args, **kwargs: CompletedProcess(args, 1, stdout="", stderr=""),
    )
    with pytest.raises(RuntimeError, match="does not descend"):
        module.reviewed_head_lineage("unrelated-branch")


def test_unrelated_file_addition_is_rejected(monkeypatch):
    module, _ = prepared(monkeypatch)
    lines = "\n".join("A\t" + p for p in module.ALLOWED_R6_AUDIT_BLOBS)
    lines = lines.replace("phase172_r6_phase_closeout/README.md",
                          "src/unreviewed.py")
    original = module.checked

    def f(*args):
        if args[:3] == ("git", "diff", "--name-status"):
            return lines
        return original(*args)

    monkeypatch.setattr(module, "checked", f)
    with pytest.raises(RuntimeError, match="unreviewed change"):
        module.reviewed_head_lineage("modified-source")


def test_modified_existing_file_is_rejected(monkeypatch):
    module, _ = prepared(monkeypatch)
    lines = "\n".join("A\t" + p for p in module.ALLOWED_R6_AUDIT_BLOBS)
    lines = lines.replace("A\tphase172_r6_phase_closeout/audit.py",
                          "M\tphase172_r6_phase_closeout/audit.py")
    original = module.checked

    def f(*args):
        if args[:3] == ("git", "diff", "--name-status"):
            return lines
        return original(*args)

    monkeypatch.setattr(module, "checked", f)
    with pytest.raises(RuntimeError, match="unreviewed change"):
        module.reviewed_head_lineage("modified-audit-file")


def test_reviewed_audit_file_content_difference_is_rejected(monkeypatch):
    module, _ = prepared(monkeypatch)
    original = module.checked

    def f(*args):
        if args[:2] == ("git", "rev-parse"):
            return "0" * 40
        return original(*args)

    monkeypatch.setattr(module, "checked", f)
    with pytest.raises(RuntimeError, match="content differs"):
        module.reviewed_head_lineage("wrong-blob")


def test_missing_or_duplicate_audit_additions_are_rejected(monkeypatch):
    module, _ = prepared(monkeypatch)
    original = module.checked
    lines = "\n".join("A\t" + p for p in module.ALLOWED_R6_AUDIT_BLOBS)
    duplicate = lines.splitlines()
    duplicate[-1] = duplicate[0]

    for changed in ("\n".join(lines.splitlines()[:-1]), "\n".join(duplicate)):
        def f(*args):
            if args[:3] == ("git", "diff", "--name-status"):
                return changed
            return original(*args)
        monkeypatch.setattr(module, "checked", f)
        with pytest.raises(RuntimeError):
            module.reviewed_head_lineage("invalid-additions")


def test_payload_is_a_complete_reviewed_replacement():
    source = PAYLOAD.read_bytes()
    assert digest(source) == CORRECTED_SHA256
    assert ORIGINAL_SHA256 != CORRECTED_SHA256
    assert b"def reviewed_head_lineage" in source
    assert b"def preflight" in source
    assert b"def apply_documents" in source
    assert b"def read_closeout_report" in source
    assert b"from .sections import APPENDS, MARKER, make_revision" in source
