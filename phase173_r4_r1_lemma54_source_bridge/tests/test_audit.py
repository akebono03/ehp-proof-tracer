"""Offline checks for source immutability and review scope."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_r4_r1_lemma54_source_bridge.audit import validate_audit_additions


def test_empty_delta_is_allowed() -> None:
    assert validate_audit_additions("") == ()


def test_only_added_phase173_files_are_allowed() -> None:
    assert validate_audit_additions(
        "A\tphase173_r4_r1_subgoal_closure/audit.py\n"
    ) == ("phase173_r4_r1_subgoal_closure/audit.py",)


@pytest.mark.parametrize("record", [
    "M\tphase173_r4_r1_subgoal_closure/audit.py",
    "A\tphase165_r52_r9_shared_math.py",
    "D\tphase173_r4_r1_subgoal_closure/audit.py",
    "A\tphase173_r4_r1_subgoal_closure/../bad.py",
    "R100\tphase173_r4_r1_subgoal_closure/x.py\tphase173_r4_r1_subgoal_closure/y.py",
])
def test_unauthorized_commit_diff_is_rejected(record: str) -> None:
    with pytest.raises(RuntimeError):
        validate_audit_additions(record)


def test_no_production_changes_in_auditor() -> None:
    path = Path(__file__).resolve().parents[1] / "audit.py"
    source = path.read_text(encoding="utf-8")
    assert "git reset" not in source
    assert "os.replace" not in source
    assert "production_changes" in source
