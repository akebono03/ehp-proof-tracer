"""Focused contract tests for the Phase 170 end-of-phase active-suite closeout."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from phase170_r3_r11_active_suite_closeout import closeout


def sample_worker(k: int) -> dict:
    return {
        "k": k, "n": 2, "group_dimension": k + 2,
        "toda52_applicable": True, "target_typed": True,
        "source_precedes": True, "search_status": "complete",
        "search_complete": True, "open_goals": 0, "proven_steps": 4,
        "result": "COMPLETE_AND_WEB_VERIFIED",
        "audit_result": "COMPLETE_AND_WEB_VERIFIED",
        "web_key": "generic-complete-proof", "web_partial": False,
        "web_steps": 4, "web_lines": 4, "web_error": None,
    }


def sample_pre() -> dict:
    return {"branch": "develop", "head": closeout.EXPECTED_HEAD,
            "worker_sha256": "reviewed-worker-hash"}


def sample_report() -> dict:
    return {
        "phase": "170 R3-R10", "mode": "AUDIT_ONLY_FRESH_33",
        "dry_run": False, "result": "DOMAIN_ALL_VERIFIED",
        "tracked_unchanged": True, "domain": list(range(1, 34)),
        "domain_checked": 33, "domain_complete": 33,
        "domain_gaps": 0,
        "preflight": {"branch": "develop", "head": closeout.EXPECTED_HEAD,
                      "tracked_changed_paths": [],
                      "worker_sha256": "reviewed-worker-hash"},
        "rows": [sample_worker(k) for k in range(1, 34)],
    }


def test_all_33_exact_rows_and_web_checks_are_accepted() -> None:
    closeout.validate_domain_report(sample_report(), sample_pre())


def test_rejects_dry_run_even_when_counts_are_33() -> None:
    report = sample_report()
    report["dry_run"] = True
    with pytest.raises(ValueError, match="provenance"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_stale_head() -> None:
    report = sample_report()
    report["preflight"]["head"] = "0" * 40
    with pytest.raises(ValueError, match="worker/HEAD"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_mismatched_worker_hash() -> None:
    report = sample_report()
    report["preflight"]["worker_sha256"] = "different"
    with pytest.raises(ValueError, match="worker/HEAD"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_gapped_or_duplicate_coordinate() -> None:
    report = sample_report()
    report["rows"][12]["k"] = 12
    with pytest.raises(ValueError, match="coordinates"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_missing_row() -> None:
    report = sample_report()
    report["rows"].pop()
    with pytest.raises(ValueError, match="surplus worker"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_false_complete_web_partial() -> None:
    report = sample_report()
    report["rows"][11]["web_partial"] = True
    with pytest.raises(ValueError, match="unverified"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_zero_proven_steps() -> None:
    report = sample_report()
    report["rows"][11]["proven_steps"] = 0
    with pytest.raises(ValueError, match="unverified"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_missing_web_lines() -> None:
    report = sample_report()
    report["rows"][11]["web_lines"] = 0
    with pytest.raises(ValueError, match="unverified"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_search_with_unresolved_goals() -> None:
    report = sample_report()
    report["rows"][11]["open_goals"] = 2
    with pytest.raises(ValueError, match="unverified"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_fake_report_counts() -> None:
    report = sample_report()
    report["domain_gaps"] = 1
    with pytest.raises(ValueError, match="counts"):
        closeout.validate_domain_report(report, sample_pre())


def test_selects_only_the_verified_full_audit(tmp_path: Path) -> None:
    old = tmp_path / "phase170_r3_r10_n2_33_20261029_045006_272086"
    new = tmp_path / "phase170_r3_r10_n2_33_20261029_045030_272086"
    old.mkdir()
    new.mkdir()
    (old / "audit.json").write_text(json.dumps(sample_report()), encoding="utf-8")
    (new / "audit.json").write_text(json.dumps({"dry_run": True}), encoding="utf-8")
    chosen, report = closeout.find_verified_report(tmp_path, sample_pre(), None)
    assert chosen == old / "audit.json"
    assert report["domain_complete"] == 33


def test_explicit_invalid_audit_file_must_not_fall_back(tmp_path: Path) -> None:
    good = tmp_path / "phase170_r3_r10_n2_33_20261029_045006_272086"
    good.mkdir()
    (good / "audit.json").write_text(json.dumps(sample_report()), encoding="utf-8")
    bad = tmp_path / "bad.json"
    bad.write_text('{"result":"DOMAIN_ALL_VERIFIED"}', encoding="utf-8")
    with pytest.raises(RuntimeError, match="no valid"):
        closeout.find_verified_report(tmp_path, sample_pre(), bad)


def test_active_pytest_command_matches_prior_phase_closure() -> None:
    assert closeout.ACTIVE_TEST_ARGS == (
        "-B", "-m", "pytest", "-q", "--tb=short",
        "--disable-warnings", "-p", "no:cacheprovider", "tests",
    )


def test_preflight_accepts_only_clean_reviewed_commit(tmp_path: Path,
                                                       monkeypatch: pytest.MonkeyPatch) -> None:
    for path in closeout.EXPECTED_BLOBS:
        p = tmp_path / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"reviewed fixture")
    (tmp_path / "tests").mkdir()
    expected = {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): closeout.EXPECTED_HEAD,
        ("diff", "--cached", "--name-only", "--"): "",
        ("diff", "--name-only", "HEAD", "--"): "",
    }
    for path, blob in closeout.EXPECTED_BLOBS.items():
        expected[("rev-parse", f"HEAD:{path}")] = blob
    monkeypatch.setattr(closeout, "git", lambda root, *args: expected[args])
    assert closeout.preflight(tmp_path, check_remote=False)["branch"] == "develop"
    expected[("diff", "--name-only", "HEAD", "--")] = "phase168_r2_toda52_transport.py"
    with pytest.raises(RuntimeError, match="tracked changes"):
        closeout.preflight(tmp_path, check_remote=False)


def test_preflight_rejects_wrong_blob(tmp_path: Path,
                                      monkeypatch: pytest.MonkeyPatch) -> None:
    for path in closeout.EXPECTED_BLOBS:
        p = tmp_path / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"fixture")
    (tmp_path / "tests").mkdir()

    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return closeout.EXPECTED_HEAD
        if args[0] == "diff":
            return ""
        if args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return "wrong-blob"
        raise AssertionError(args)

    monkeypatch.setattr(closeout, "git", fake_git)
    with pytest.raises(RuntimeError, match="blob"):
        closeout.preflight(tmp_path, check_remote=False)


def test_full_pytest_streams_logs_without_running_early(tmp_path: Path,
                                                        monkeypatch: pytest.MonkeyPatch) -> None:
    captured = {}

    class FakeProcess:
        stdout = iter(["... [100%]\n", "3546 passed in 30.00s\n"])

        def wait(self) -> int:
            return 0

    def fake_popen(command, **kwargs):
        captured["command"] = command
        captured["env"] = kwargs["env"]
        return FakeProcess()

    monkeypatch.setattr(closeout.subprocess, "Popen", fake_popen)
    rc, summary = closeout.run_active_tests(tmp_path, tmp_path / "full_pytest.log")
    assert rc == 0 and "3546 passed" in summary
    assert captured["command"] == [closeout.sys.executable, *closeout.ACTIVE_TEST_ARGS]
    assert captured["env"]["PYTHONUTF8"] == "1"
    assert (tmp_path / "full_pytest.log").read_text(encoding="utf-8").endswith("3546 passed in 30.00s\n")


def test_worker_requires_real_web_proof_not_only_headline() -> None:
    row = deepcopy(sample_worker(12))
    assert closeout.valid_worker_row(row, 12)
    row["web_key"] = "partial-proof"
    assert not closeout.valid_worker_row(row, 12)
