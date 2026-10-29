"""Isolated contract tests for R3-R8R2. No application imports required."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase170_r3_r8r2_k12_utf8_recheck import runner


def previous_report() -> dict:
    rows = [{"k": 0, "result": "OUTSIDE_TODA_5_2_DOMAIN"}]
    rows += [{"k": k, "result": "WORKER_FAILED" if k == 12 else "COMPLETE_AND_WEB_VERIFIED"}
             for k in range(1, 34)]
    return {"preflight": {"branch": "develop", "head": "f479e0aabdfeefa69ad986e20c0f69ce0efd7bbd"},
            "rows": rows, "domain_checked": 33, "domain_complete": 32, "domain_gaps": 1,
            "tracked_unchanged": True}


def test_reviewed_previous_report_is_eligible():
    assert runner.eligible_prior_report(previous_report())


def test_incomplete_previous_report_is_rejected():
    report = previous_report()
    report["domain_complete"] = 33
    assert not runner.eligible_prior_report(report)


def test_unrelated_failure_is_rejected():
    report = previous_report()
    report["rows"][13]["result"] = "WORKER_EXCEPTION"
    assert not runner.eligible_prior_report(report)


def test_worker_utf8_json_parses_subscripts():
    raw = runner.SENTINEL + json.dumps({"k": 12, "result": "COMPLETE_AND_WEB_VERIFIED", "note": "η₂"}, ensure_ascii=False)
    assert runner.parse_worker_output(raw, 0)["note"] == "η₂"


def test_worker_wrong_exit_is_not_complete():
    raw = runner.SENTINEL + json.dumps({"k": 12, "result": "COMPLETE_AND_WEB_VERIFIED"})
    assert runner.parse_worker_output(raw, 1)["result"] == "WORKER_FAILED"


def test_worker_multiple_sentinels_is_rejected():
    raw = runner.SENTINEL + '{"k": 12}\n' + runner.SENTINEL + '{"k": 12}'
    assert runner.parse_worker_output(raw, 0)["result"] == "WORKER_FAILED"


def test_combined_33_success_preserves_prior_results():
    report = previous_report()
    row = {"k": 12, "result": "COMPLETE_AND_WEB_VERIFIED", "proof_steps": 3}
    joined = runner.combine(report, row)
    assert joined["scope"] == "COMBINED_33_K"
    assert joined["checked"] == 33
    assert joined["complete"] == 33
    assert joined["gaps"] == 0
    assert joined["rows"][11] == report["rows"][11]
    assert joined["rows"][12]["proof_steps"] == 3


def test_combined_gap_remains_visible():
    joined = runner.combine(previous_report(), {"k": 12, "result": "PROOF_UNFINISHED"})
    assert joined["checked"] == 33 and joined["complete"] == 32 and joined["gaps"] == 1


def test_single_k_result_if_previous_audit_missing():
    result = runner.combine(None, {"k": 12, "result": "COMPLETE_AND_WEB_VERIFIED"})
    assert result["scope"] == "SINGLE_K" and result["checked"] == 1


def test_preflight_accepts_only_reviewed_clean_commit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    for f in runner.EXPECTED_BLOBS:
        p = tmp_path / f
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"fixture")
    answers = {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): runner.EXPECTED_HEAD,
        ("diff", "--name-only"): "",
        ("diff", "--cached", "--name-only"): "",
    }
    for path, sha in runner.EXPECTED_BLOBS.items():
        answers[("rev-parse", f"HEAD:{path}")] = sha
    monkeypatch.setattr(runner, "git", lambda _root, *args: answers[args])
    result = runner.preflight(tmp_path)
    assert result["head"] == runner.EXPECTED_HEAD
    answers[("diff", "--name-only")] = "phase168_r2_toda52_transport.py"
    with pytest.raises(RuntimeError, match="unstaged tracked changes"):
        runner.preflight(tmp_path)


def test_prior_report_discovery(tmp_path: Path):
    folder = tmp_path / "phase170_r3_r8_n2_old"
    folder.mkdir()
    (folder / "audit.json").write_text(json.dumps(previous_report()), encoding="utf-8")
    result = runner.find_prior_report(tmp_path)
    assert result is not None and result[0] == folder / "audit.json"


def test_worker_subprocess_forces_utf8(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from types import SimpleNamespace

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(runner, "preflight", lambda root: {"branch": "develop", "head": runner.EXPECTED_HEAD})
    monkeypatch.setattr(runner, "find_prior_report", lambda root: None)
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["env"] = kwargs["env"]
        output = runner.SENTINEL + json.dumps(
            {"k": 12, "result": "COMPLETE_AND_WEB_VERIFIED", "note": "η₂"},
            ensure_ascii=False,
        ) + "\n"
        return SimpleNamespace(stdout=output, returncode=0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    assert runner.run(tmp_path, dry_run=False, timeout_seconds=60) == 0
    assert captured["env"]["PYTHONIOENCODING"] == "utf-8"
    assert captured["env"]["PYTHONUTF8"] == "1"
    assert captured["command"][-2:] == ["--k", "12"]
    reports = list((tmp_path / "EHPProofTracerRecovery").glob("phase170_r3_r8r2_k12_*/audit.json"))
    assert len(reports) == 1
    result = json.loads(reports[0].read_text(encoding="utf-8"))
    assert result["worker_row"]["note"] == "η₂"
    assert result["tracked_unchanged"] is True
