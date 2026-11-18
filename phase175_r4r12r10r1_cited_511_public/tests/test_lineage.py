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
