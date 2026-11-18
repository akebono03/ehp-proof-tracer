"""Focused regression contracts for the reviewed R10R1R2 Git handoff."""
from __future__ import annotations

import pytest

from phase175_r4r12r10r1_cited_511_public import audit, installer


def test_reviewed_r9_commit_exact_change_set_is_accepted() -> None:
    assert audit.validate_reviewed_lineage(
        audit.REVIEWED_R9_HEAD, audit.REVIEWED_R9_COMMITTED_PATHS, True, 1,
    ) == "R9_REVIEWED_COMMITTED"
    assert installer.REVIEWED_R9_COMMITTED_BLOB == "83f278ec98512a763cdfba2552c70f972b169eac"


def test_prior_head_is_accepted_only_without_later_commits() -> None:
    assert audit.validate_reviewed_lineage(
        audit.REVIEWED_HEAD, frozenset(), True, 0,
    ) == "R9_LOCAL_PATCH_BEFORE_COMMIT"
    with pytest.raises(RuntimeError, match="OLD_HEAD_DIFF"):
        audit.validate_reviewed_lineage(
            audit.REVIEWED_HEAD, audit.REVIEWED_R9_COMMITTED_PATHS, True, 1,
        )


def test_r9_commit_drift_and_unreviewed_head_are_rejected() -> None:
    with pytest.raises(RuntimeError, match="R9_COMMIT_DIFF"):
        audit.validate_reviewed_lineage(
            audit.REVIEWED_R9_HEAD, frozenset(), True, 1,
        )
    with pytest.raises(RuntimeError, match="R9_COMMIT_DIFF"):
        audit.validate_reviewed_lineage(
            audit.REVIEWED_R9_HEAD, audit.REVIEWED_R9_COMMITTED_PATHS, False, 1,
        )
    with pytest.raises(RuntimeError, match="UNREVIEWED_HEAD"):
        audit.validate_reviewed_lineage("0" * 40, frozenset(), False, 0)


def test_reviewed_r10_diagnostic_commit_is_accepted() -> None:
    assert audit.REVIEWED_R10_HEAD == "12d2116bc23e96c879d97b043dbc104b31030091"
    cumulative = audit.REVIEWED_R9_COMMITTED_PATHS | audit.REVIEWED_R10_COMMITTED_PATHS
    assert audit.validate_reviewed_lineage(
        audit.REVIEWED_R10_HEAD, cumulative, True, 2,
    ) == "R10_R3_REVIEWED_COMMITTED"
    assert installer.REVIEWED_R9_COMMITTED_BLOB == "83f278ec98512a763cdfba2552c70f972b169eac"


def test_reviewed_r10_commit_requires_exact_files_ancestry_and_count() -> None:
    cumulative = audit.REVIEWED_R9_COMMITTED_PATHS | audit.REVIEWED_R10_COMMITTED_PATHS
    for files, ancestor, count in (
        (frozenset(), True, 2),
        (cumulative - {".pytest_cache/v/cache/nodeids"}, True, 2),
        (cumulative | {"unreviewed.py"}, True, 2),
        (cumulative, False, 2),
        (cumulative, True, 1),
        (cumulative, True, 3),
    ):
        with pytest.raises(RuntimeError, match="R10_COMMIT_DIFF"):
            audit.validate_reviewed_lineage(
                audit.REVIEWED_R10_HEAD, files, ancestor, count,
            )


def test_reviewed_r10_overlay_is_the_only_extra_dirty_allowlist() -> None:
    assert audit.REVIEWED_R10_LOCAL_OVERLAY == {
        "phase175_r4r12r10r1_cited_511_public/AUDIT_PLAN_JA.md",
        "phase175_r4r12r10r1_cited_511_public/CODE_FULL_JA.md",
        "phase175_r4r12r10r1_cited_511_public/README.md",
        "phase175_r4r12r10r1_cited_511_public/audit.py",
        "phase175_r4r12r10r1_cited_511_public/provider.py",
        "phase175_r4r12r10r1_cited_511_public/tests/test_cited_511.py",
        "phase175_r4r12r10r1_cited_511_public/tests/test_lineage.py",
        "phase175_r4r12r10r1_cited_511_public/output/preflight.json",
    }
    assert audit.validate_reviewed_local_changes(set(audit.REVIEWED_R10_LOCAL_OVERLAY)) == sorted(audit.REVIEWED_R10_LOCAL_OVERLAY)


def test_unreviewed_tracked_sources_still_rejected() -> None:
    for unexpected in (
        "phase175_r4r12r10r1_cited_511_public/source.py",
        "phase175_r4r12r10r1_cited_511_public/installer.py",
        "phase175_r4r12r10r1_cited_511_public/run.ps1",
        "phase175_r4r12r10r1_cited_511_public/output/audit_report.json",
        "phase175_r4r12r10r1_cited_511_public/unknown.py",
        "proof.py",
    ):
        with pytest.raises(RuntimeError, match="UNREVIEWED_TRACKED_CHANGES"):
            audit.validate_reviewed_local_changes({unexpected})


def test_production_and_pytest_cache_remain_existing_exceptions() -> None:
    accepted = {str(installer.TARGET), ".pytest_cache/v/cache/nodeids"}
    assert audit.validate_reviewed_local_changes(accepted) == sorted(accepted)
