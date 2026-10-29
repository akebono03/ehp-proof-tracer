"""Focused read-only R1D report extraction tests."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase171_r1d_k3_three_gap_diagnostics import triage


def sample_report() -> dict:
    ns = [2, 3, 4, 5, 6, 7] + list(range(9, 60, 2))
    assert len(ns) == 32
    rows = []
    for n in ns:
        unfinished = n in (3, 4, 5)
        rows.append({
            "n": n, "k": 3, "group_dimension": n + 3,
            "result": "PROOF_UNFINISHED" if unfinished else "COMPLETE_AND_WEB_VERIFIED",
            "target_typed": True,
            "target_type": "Relation",
            "target_coordinates": [n, 3],
            "search_status": "partial" if unfinished else "complete",
            "proven_steps": 1 if unfinished else 3,
            "open_goals": 2 if unfinished else 0,
            "open_goal_samples": [f"未解決目標 {n}"] if unfinished else [],
            "diagnostics": [f"診断 {n}"] if unfinished else [],
            "root_conclusion_matches_target": not unfinished,
            "search_complete": not unfinished,
            "web_key": "partial-proof" if unfinished else "generic-complete-proof",
            "web_partial": unfinished,
            "web_steps": 1 if unfinished else 3,
            "web_lines": 1 if unfinished else 4,
            "web_error": None,
        })
    return {
        "phase": "171 R1C", "stem": 3, "dry_run": False,
        "result": "AUDIT_COMPLETE_WITH_GAPS", "tracked_unchanged": True,
        "preflight": {"head": triage.EXPECTED_HEAD},
        "domain": [{"n": n, "k": 3, "csv_rows": 2 if n == 4 else 1} for n in ns],
        "rows": rows, "domain_checked": 32, "domain_complete": 29,
        "domain_gaps": 3, "worker_failures": 0,
    }


def test_extracts_only_three_incomplete_registered_goals() -> None:
    gaps = triage.validate_report(sample_report())
    assert tuple(row["n"] for row in gaps) == (3, 4, 5)
    assert all(row["result"] == "PROOF_UNFINISHED" for row in gaps)


def test_preserves_original_diagnostics_and_open_goals() -> None:
    details = triage.extract_details(triage.validate_report(sample_report()))
    assert details[0]["open_goal_samples"] == ["未解決目標 3"]
    assert details[1]["diagnostics"] == ["診断 4"]
    assert details[2]["web_key"] == "partial-proof"


def test_rejects_dry_run_report() -> None:
    sample = sample_report()
    sample["dry_run"] = True
    with pytest.raises(ValueError, match="dry-run"):
        triage.validate_report(sample)


def test_rejects_wrong_stem() -> None:
    sample = sample_report()
    sample["stem"] = 2
    with pytest.raises(ValueError, match="stem"):
        triage.validate_report(sample)


def test_rejects_wrong_reviewed_head() -> None:
    sample = sample_report()
    sample["preflight"]["head"] = "wrong"
    with pytest.raises(ValueError, match="HEAD"):
        triage.validate_report(sample)


def test_rejects_missing_worker_row() -> None:
    sample = sample_report()
    sample["rows"].pop()
    with pytest.raises(ValueError, match="32"):
        triage.validate_report(sample)


def test_rejects_duplicate_registered_coordinates() -> None:
    sample = sample_report()
    sample["domain"][2]["n"] = 3
    with pytest.raises(ValueError, match="worker row"):
        triage.validate_report(sample)


def test_rejects_inconsistent_summary() -> None:
    sample = sample_report()
    sample["domain_complete"] = 30
    with pytest.raises(ValueError, match="summary counters"):
        triage.validate_report(sample)


def test_rejects_unexpected_gap_in_fully_checked_report() -> None:
    sample = sample_report()
    sample["rows"][0]["result"] = "PROOF_UNFINISHED"
    sample["domain_complete"] = 28
    sample["domain_gaps"] = 4
    with pytest.raises(ValueError, match="unexpected gap"):
        triage.validate_report(sample)


def test_categories_are_observations_not_mathematical_conclusions() -> None:
    row = sample_report()["rows"][1]
    assert triage.diagnostic_category(row) == "SEARCH_UNFINISHED"
    assert triage.diagnostic_category({**row, "target_typed": False}) == "TYPED_GOAL_NOT_RESOLVED"
    assert triage.diagnostic_category({**row, "search_status": "complete", "open_goals": 0}) == "CONCLUSION_NOT_MATCHED"
    assert triage.diagnostic_category({**row, "search_status": "complete", "open_goals": 0,
                                       "root_conclusion_matches_target": True}) == "WEB_VERIFICATION_NOT_COMPLETE"


def test_markdown_contains_three_specific_goals() -> None:
    details = triage.extract_details(triage.validate_report(sample_report()))
    md = triage.render_markdown(details, Path("audit.json"))
    for n in (3, 4, 5):
        assert f"\\pi_{{{n + 3}}}^{{{n}}}" in md
    assert "診断 4" in md
    assert "未解決目標 3" in md


def test_dry_run_does_not_write_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    report = tmp_path / "audit.json"
    report.write_text(json.dumps(sample_report(), ensure_ascii=False), encoding="utf-8")
    git_state = {"branch": "develop", "head": triage.EXPECTED_HEAD, "tracked_clean": True}
    monkeypatch.setattr(triage, "tracked_state", lambda root: git_state)
    assert triage.run(tmp_path, report, dry_run=True) == 0
    assert sorted(p.name for p in tmp_path.iterdir()) == ["audit.json"]


def test_report_writes_only_to_recovery(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    report = tmp_path / "audit.json"
    report.write_text(json.dumps(sample_report(), ensure_ascii=False), encoding="utf-8")
    git_state = {"branch": "develop", "head": triage.EXPECTED_HEAD, "tracked_clean": True}
    monkeypatch.setattr(triage, "tracked_state", lambda root: git_state)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "external_recovery"))
    assert triage.run(tmp_path, report) == 0
    output = next((tmp_path / "external_recovery" / "EHPProofTracerRecovery").iterdir())
    assert (output / "gap_details.json").is_file()
    assert (output / "gap_details.md").is_file()
    assert json.loads((output / "gap_details.json").read_text(encoding="utf-8"))["checked"] == 32


def test_tracked_state_accepts_both_reviewed_clean_heads(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A post-audit commit may add audit files without invalidating the old report."""
    import subprocess

    for head in (triage.EXPECTED_HEAD, triage.REVIEWED_CURRENT_HEAD):
        def git_result(root: Path, *args: str) -> str:
            commands = {
                ("branch", "--show-current"): "develop",
                ("rev-parse", "HEAD"): head,
                ("rev-parse", "--verify", "refs/remotes/origin/develop"): head,
                ("status", "--porcelain", "--untracked-files=no"): "",
            }
            return commands[args]

        monkeypatch.setattr(triage, "git", git_result)
        monkeypatch.setattr(
            subprocess, "run", lambda *a, **kw:
            subprocess.CompletedProcess(args=a, returncode=0, stdout=b"", stderr=b""),
        )
        state = triage.tracked_state(tmp_path)
        assert state["head"] == head
        assert state["origin_develop"] == head
        assert state["tracked_clean"] is True


def test_tracked_state_rejects_unreviewed_head(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    unreviewed = "f" * 40
    def git_result(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        return unreviewed
    monkeypatch.setattr(triage, "git", git_result)
    with pytest.raises(RuntimeError, match="unexpected Git state"):
        triage.tracked_state(tmp_path)


def test_tracked_state_rejects_origin_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    def git_result(root: Path, *args: str) -> str:
        commands = {
            ("branch", "--show-current"): "develop",
            ("rev-parse", "HEAD"): triage.REVIEWED_CURRENT_HEAD,
            ("rev-parse", "--verify", "refs/remotes/origin/develop"): triage.EXPECTED_HEAD,
        }
        return commands[args]
    monkeypatch.setattr(triage, "git", git_result)
    with pytest.raises(RuntimeError, match="unexpected Git state"):
        triage.tracked_state(tmp_path)


def test_tracked_state_rejects_modified_tracked_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    def git_result(root: Path, *args: str) -> str:
        commands = {
            ("branch", "--show-current"): "develop",
            ("rev-parse", "HEAD"): triage.REVIEWED_CURRENT_HEAD,
            ("rev-parse", "--verify", "refs/remotes/origin/develop"): triage.REVIEWED_CURRENT_HEAD,
            ("status", "--porcelain", "--untracked-files=no"): " M web_group_proof.py",
        }
        return commands[args]
    monkeypatch.setattr(triage, "git", git_result)
    with pytest.raises(RuntimeError, match="tracked files"):
        triage.tracked_state(tmp_path)


def test_old_r1c_report_head_remains_pinned_after_git_review_update() -> None:
    assert triage.EXPECTED_HEAD != triage.REVIEWED_CURRENT_HEAD
    assert triage.validate_report(sample_report())
    report = sample_report()
    report["preflight"]["head"] = triage.REVIEWED_CURRENT_HEAD
    with pytest.raises(ValueError, match="unexpected reviewed HEAD"):
        triage.validate_report(report)
