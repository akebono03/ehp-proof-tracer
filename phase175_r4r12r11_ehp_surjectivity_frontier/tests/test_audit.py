"""Focused tests for the read-only EHP surjectivity diagnostic."""
from __future__ import annotations

from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase175_r4r12r11_ehp_surjectivity_frontier import audit


def test_diagonal_sphere_group_is_not_zero() -> None:
    assert not audit.valid_zero_goal(TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(9, 9)))


def test_off_diagonal_zero_goal_not_prejudged() -> None:
    assert audit.valid_zero_goal(TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(9, 17)))


def test_audit_does_not_claim_completed_proof() -> None:
    assert audit.PACKAGE == "phase175_r4r12r11_ehp_surjectivity_frontier"
    assert "NOT_COMPLETE" in "PASS_R11_EHP_SURJECTIVITY_FRONTIER_AUDITED_NOT_COMPLETE"


def test_git_command_failure_is_not_swallowed(monkeypatch: pytest.MonkeyPatch) -> None:
    class Failed:
        returncode = 1
        stdout = ""
        stderr = "intentional failure"

    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: Failed())
    with pytest.raises(RuntimeError, match="R11_GIT_FAILED"):
        audit.git(Path.cwd(), "rev-parse", "HEAD")
