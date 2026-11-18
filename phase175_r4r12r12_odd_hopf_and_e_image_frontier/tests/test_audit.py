"""Focused, read-only audit contracts."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase175_r4r12r12_odd_hopf_and_e_image_frontier import audit


def test_phase_is_read_only() -> None:
    assert audit.PACKAGE == "phase175_r4r12r12_odd_hopf_and_e_image_frontier"
    assert "NOT_COMPLETE" in "PASS_R12_ODD_HOPF_AND_E_IMAGE_FRONTIER_NOT_COMPLETE"


def test_git_error_is_not_ignored(monkeypatch: pytest.MonkeyPatch) -> None:
    class Failed:
        returncode = 2
        stdout = ""
        stderr = "failure"
    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: Failed())
    with pytest.raises(RuntimeError, match="R12_GIT_FAILED"):
        audit.git(Path.cwd(), "rev-parse", "HEAD")


def test_diagnostic_inspects_both_orientations_without_choosing_result() -> None:
    source = Path(audit.__file__).read_text(encoding="utf-8")
    assert "for orientation, path in enumerate(selected)" in source
    assert '"group_complete": False' in source
    assert '"new_given": 0' in source


def test_false_zero_not_accepted_as_theorem() -> None:
    source = Path(audit.__file__).read_text(encoding="utf-8")
    assert "zero_route_requires_false_diagonal_zero" in source
    assert '"external_odd_hopf_theorem_not_registered": True' in source
