"""Offline tests for Phase 173 R3 portable, read-only report inspection."""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_r3_portable import audit


def test_added_phase173_paths_are_allowed() -> None:
    assert audit.verify_committed_changes(
        "A\tphase173_r1_nge3_audit/audit.py\n"
        "A\tphase173_r3_head_guard_fix/audit.py\n"
    ) == ("phase173_r1_nge3_audit/audit.py", "phase173_r3_head_guard_fix/audit.py")


@pytest.mark.parametrize("entry", [
    "M\tphase165_r52_r9_shared_math.py",
    "A\tsources/toda/new.tex",
    "D\tphase173_r1_nge3_audit/audit.py",
    "R100\tphase173_r1_nge3_audit/old.py\tphase173_r1_nge3_audit/new.py",
    "A\tdocs/development_log.md",
    "A\tphase173_invalid/../bad.py",
])
def test_other_changes_are_rejected(entry: str) -> None:
    with pytest.raises(RuntimeError):
        audit.verify_committed_changes(entry)


def test_preflight_accepts_new_head_with_only_reviewed_additions(monkeypatch, tmp_path: Path) -> None:
    source = tmp_path / "sources" / "toda" / "Toda_05_2.tex"
    source.parent.mkdir(parents=True)
    source.write_text(
        r"\begin{proposition}\label{prop:5.6}\pi^{4}_{7}\pi^{n}_{n+3}\nu'\end{proposition}",
        encoding="utf-8",
    )
    current = "new-head"
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args in (("rev-parse", "HEAD"), ("rev-parse", "origin/develop")):
            return current
        if args[:3] == ("diff", "--name-status", "--no-renames"):
            return "A\tphase173_r1_nge3_audit/audit.py"
        if args == ("status", "--porcelain", "--untracked-files=no"):
            return ""
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return audit.REVIEWED_BLOBS[args[1][5:]]
        raise AssertionError(args)
    monkeypatch.setattr(audit, "git", fake_git)
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0))
    result = audit.preflight(tmp_path)
    assert result["head"] == current
    assert len(result["reviewed_source_blobs"]) == 6


def test_preflight_rejects_changed_reviewed_blob(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "git", lambda root, *args: (
        "bad" if args[0] == "rev-parse" and args[1].startswith("HEAD:")
        else "develop" if args[0] == "branch"
        else "head" if args[0] == "rev-parse"
        else ""
    ))
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0))
    with pytest.raises(RuntimeError, match="Reviewed source content changed"):
        audit.preflight(tmp_path)


def test_missing_r1_profile_is_not_fabricated(tmp_path: Path) -> None:
    assert audit.r1_baseline_status(tmp_path) == "NOT_AVAILABLE_IN_THIS_PROFILE"


def test_valid_r1_baseline_detected(tmp_path: Path) -> None:
    directory = tmp_path / "EHPProofTracerRecovery" / "phase173_r1_example"
    directory.mkdir(parents=True)
    (directory / "audit.json").write_text(json.dumps({"rows": [
        {"n": n, "k": k, "audit_result": "PROOF_UNFINISHED"}
        for n, k in audit.TARGETS
    ]}), encoding="utf-8")
    assert audit.r1_baseline_status(tmp_path).startswith("MATCHED:")


def test_inconsistent_r1_baseline_is_rejected(tmp_path: Path) -> None:
    directory = tmp_path / "EHPProofTracerRecovery" / "phase173_r1_example"
    directory.mkdir(parents=True)
    (directory / "audit.json").write_text(json.dumps({"rows": [
        {"n": 4, "k": 3, "audit_result": "COMPLETE_AND_WEB_VERIFIED"},
        {"n": 5, "k": 3, "audit_result": "PROOF_UNFINISHED"},
    ]}), encoding="utf-8")
    with pytest.raises(RuntimeError, match="disagrees"):
        audit.r1_baseline_status(tmp_path)


def test_format_reports_roots_and_subgoals() -> None:
    rows = [{"n": 4, "k": 3, "source_locator": "Proposition 5.6",
             "screened_given_count": 26, "root_candidate_count": 1,
             "roots": [{"rule": "mock source rule", "children": [{
                 "type": "Relation", "repr": "target", "child_proposal_count": 0,
                 "exact_screened_given": False, "child_proposal_rules": [],
             }]}], "prior_sources": [
                 {"n": 3, "eligible": True, "reason": "prior_fixed_source"}
             ]}]
    output = audit.format_report(rows)
    assert "ROOT 1" in output
    assert "SUBGOAL Relation proposals=0 exact_given=False" in output
    assert "PRIOR n=3 eligible=True" in output
    assert "OBSERVATION_IS_NOT_A_PROOF=True" in output


def test_duplicate_goal_is_not_probed() -> None:
    text = audit.format_report([{"n": 5, "k": 3,
        "source_locator": "Proposition 5.6", "screened_given_count": 27,
        "root_candidate_count": 1, "roots": [{"rule": "r", "children": [
            {"type": "Relation", "repr": "test", "duplicate_subgoal": True}
        ]}], "prior_sources": []}])
    assert "proposals=DUPLICATE" in text
