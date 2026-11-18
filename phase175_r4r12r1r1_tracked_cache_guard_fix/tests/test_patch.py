from __future__ import annotations

import pytest

from phase175_r4r12r1r1_tracked_cache_guard_fix.patch import OLD, NEW, COMMITTED_PRODUCTION_BLOB, patch_text

INSTALLER = '''HEAD = "''' + OLD + '''"

def check(root):
    if git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != previous.BASE_WORKING_BLOB:
        raise RuntimeError("base")
    if git(root, "rev-parse", "HEAD") != HEAD:
        raise RuntimeError("unreviewed")
'''
AUDIT = '''HEAD = installer.HEAD

def preflight(root):
    if head != HEAD:
        raise RuntimeError("unreviewed")

def validate_prior(report):
    before = report.get("preflight")
    if (not isinstance(before, dict) or before.get("head") != HEAD):
        raise RuntimeError("invalid")
'''


def test_head_and_historical_evidence_are_separate() -> None:
    updated_installer, updated_audit = patch_text(INSTALLER, AUDIT)
    assert 'HEAD = "' + NEW + '"' in updated_installer
    assert 'before.get("head") != "' + OLD + '"' in updated_audit
    assert "if head != HEAD:" in updated_audit
    assert COMMITTED_PRODUCTION_BLOB in updated_installer


def test_idempotent() -> None:
    once = patch_text(INSTALLER, AUDIT)
    assert patch_text(*once) == once


def test_changed_prior_guard_is_rejected() -> None:
    with pytest.raises(RuntimeError, match="UNEXPECTED_PRIOR_VALIDATION"):
        patch_text(INSTALLER, AUDIT.replace('before.get("head") != HEAD', 'before.get("head") != "0"'))


def test_changed_installer_head_is_rejected() -> None:
    with pytest.raises(RuntimeError, match="UNEXPECTED_INSTALLER_HEAD"):
        patch_text(INSTALLER.replace(OLD, "0" * 40), AUDIT)



def test_only_reviewed_tracked_paths_are_permitted() -> None:
    from phase175_r4r12r1r1_tracked_cache_guard_fix.patch import reviewed_tracked_changes
    assert reviewed_tracked_changes(["phase165_r52_r9_shared_math.py", ".pytest_cache/v/cache/nodeids"]) == [
        ".pytest_cache/v/cache/nodeids", "phase165_r52_r9_shared_math.py"
    ]


def test_unrelated_tracked_change_still_fails_closed() -> None:
    from phase175_r4r12r1r1_tracked_cache_guard_fix.patch import reviewed_tracked_changes
    with pytest.raises(RuntimeError, match="proof.py"):
        reviewed_tracked_changes(["proof.py"])
