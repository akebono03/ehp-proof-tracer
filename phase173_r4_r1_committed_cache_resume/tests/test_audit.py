"""Focused failure-closed tests: the exact R4-R1 committed-cache boundary."""
from __future__ import annotations

import hashlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_r4_r1_committed_cache_resume import audit


def test_reviewed_r3_additions() -> None:
    report = audit.verify_audit_only_changes(
        "A\tphase173_r3_portable/audit.py\n"
        "A\tphase173_r3_frontier_readout/readout.py\n"
    )
    assert report["audits_added"] == [
        "phase173_r3_portable/audit.py",
        "phase173_r3_frontier_readout/readout.py",
    ]
    assert report["committed_cache_exception"] == []


def test_committed_cache_and_r4_audit_are_accepted() -> None:
    report = audit.verify_audit_only_changes(
        "M\t.pytest_cache/v/cache/nodeids\n"
        "A\tphase173_r4_r1_audit_only/audit.py\n"
        "A\tphase173_r4_r1_git_status_diagnostic/run.ps1\n"
    )
    assert report["committed_cache_exception"] == [audit.COMMITTED_CACHE]
    assert len(report["audits_added"]) == 2


@pytest.mark.parametrize("record", [
    "M\tphase165_r52_r9_shared_math.py",
    "A\tphase173_r4_r1_committed_cache_resume/audit.py",
    "A\tphase173_r5_audit/bad.py",
    "D\tphase173_r3_portable/audit.py",
    "R100\told.py\tnew.py",
    "M\tREADME.md",
    "A\tphase173_r3_portable/../wrong.py",
    "M\t.pytest_cache/v/cache/lastfailed",
    "A\t.pytest_cache/v/cache/nodeids",
])
def test_disallowed_commit_paths_fail(record: str) -> None:
    with pytest.raises(RuntimeError, match="Non-audit committed|Unexpected Git diff"):
        audit.verify_audit_only_changes(record)


def test_duplicate_committed_path_fails() -> None:
    with pytest.raises(RuntimeError, match="Duplicate"):
        audit.verify_audit_only_changes("M\t.pytest_cache/v/cache/nodeids\nM\t.pytest_cache/v/cache/nodeids")


def test_clean_worktree_ok(tmp_path: Path) -> None:
    assert audit.verify_tracked_worktree(tmp_path, "") == ()


def test_unstaged_cache_ok(tmp_path: Path) -> None:
    assert audit.verify_tracked_worktree(tmp_path, " M .pytest_cache/v/cache/nodeids\n") == (audit.COMMITTED_CACHE,)


def test_exact_reviewed_prior_patch_accepted(tmp_path: Path) -> None:
    path = "phase173_r4_r1_audit_only/audit.py"
    # If the prior correction package is unavailable (portable unzip), verify
    # the exact-digest code path by substituting a known synthetic digest.
    target = tmp_path / path
    target.parent.mkdir(parents=True)
    target.write_bytes(b"verified local audit patch\n")
    expected = hashlib.sha256(target.read_bytes()).hexdigest()
    saved = audit.APPROVED_WORKTREE_AUDIT_SHA256[path]
    try:
        audit.APPROVED_WORKTREE_AUDIT_SHA256[path] = expected
        assert audit.verify_tracked_worktree(tmp_path, " M " + path) == (path,)
    finally:
        audit.APPROVED_WORKTREE_AUDIT_SHA256[path] = saved


def test_reviewed_patch_mismatch_fails(tmp_path: Path) -> None:
    path = "phase173_r4_r1_audit_only/audit.py"
    target = tmp_path / path
    target.parent.mkdir(parents=True)
    target.write_bytes(b"unverified")
    with pytest.raises(RuntimeError, match="reviewed audit content differs"):
        audit.verify_tracked_worktree(tmp_path, " M " + path)


@pytest.mark.parametrize("status", [
    "M  .pytest_cache/v/cache/nodeids",
    "MM .pytest_cache/v/cache/nodeids",
    " D .pytest_cache/v/cache/nodeids",
    " M phase165_r52_r9_shared_math.py",
    " M .pytest_cache/v/cache/lastfailed",
    "?? .pytest_cache/v/cache/nodeids",
    " M .pytest_cache/v/cache/nodeids\n M README.md",
])
def test_unapproved_worktree_fails(tmp_path: Path, status: str) -> None:
    with pytest.raises(RuntimeError):
        audit.verify_tracked_worktree(tmp_path, status)


def test_git_porcelain_preserves_leading_space(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=" M .pytest_cache/v/cache/nodeids\n"))
    assert audit.git(tmp_path, "status", "--porcelain", "--untracked-files=no") == " M .pytest_cache/v/cache/nodeids"


def test_named_function_read_only() -> None:
    report = audit.inspect_named_function("def sample(x):\n    return x\n", "sample")
    assert report["defined_exactly_once"] is True
    assert report["mentions_direct_sum"] is False


def test_toda_equation_does_not_certify_pi77() -> None:
    ch5 = (
        "Prop 4.4 とLem 5.4 から,\n"
        "\\begin{equation}\\label{eq:5.6}\n"
        "\\pi^{\\,3}_{i-1}\\oplus\\pi^{\\,7}_{i} "
        "\\xrightarrow{\\cong}\\pi_{\\,i}^{4} "
        "\\nu_{4}\\circ\\beta\n"
        "\\end{equation}\n"
        "H(\\nu_{4})=\\iota_7, 2E \\nu_{4}=E^{2}\\nu'"
    )
    ch4 = "\\begin{proposition}\\label{prop:4.4}\n\\pit{i-1}{n-1}\\oplus\\pit{i}{2n-1} 同型\n\\end{proposition}"
    assert audit.verify_source_text(ch5, ch4)["pi77_free_cyclic_proved_here"] is False
