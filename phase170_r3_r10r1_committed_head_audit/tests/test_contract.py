"""Focused contract tests; never import or alter application modules."""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase170_r3_r10r1_committed_head_audit import audit


def complete_row(k: int) -> dict:
    return {
        "k": k, "n": 2, "group_dimension": k + 2,
        "toda52_applicable": True, "target_typed": True,
        "source_precedes": True, "result": "COMPLETE_AND_WEB_VERIFIED",
        "search_complete": True, "search_status": "complete", "open_goals": 0,
        "proven_steps": 4 if k == 12 else 3,
        "web_key": "generic-complete-proof", "web_partial": False,
        "web_steps": 2, "web_lines": 3, "web_error": None,
    }


def test_domain_exactly_thirty_three_positive_stems() -> None:
    assert audit.DOMAIN == tuple(range(1, 34))
    assert 0 not in audit.DOMAIN


def test_explicit_n2_db_rows_are_required(tmp_path: Path) -> None:
    source = tmp_path / "sphere.csv"
    source.write_text("k,n,id\n" + "".join(f"{k},2,0\n" for k in range(34)), encoding="utf-8-sig")
    assert audit.explicit_n2_stems(source) == tuple(range(34))
    source.write_text("k,n,id\n" + "".join(f"{k},2,0\n" for k in range(33)), encoding="utf-8-sig")
    with pytest.raises(RuntimeError, match="33"):
        audit.explicit_n2_stems(source)


def test_worker_output_must_be_one_typed_utf8_row() -> None:
    text = audit.SENTINEL + json.dumps({**complete_row(12), "note": "η₂"}, ensure_ascii=False)
    result = audit.parse_worker_output(text, 0, 12)
    assert result["audit_result"] == "COMPLETE_AND_WEB_VERIFIED"
    assert result["note"] == "η₂"
    assert audit.parse_worker_output(text, 1, 12)["audit_result"] == "WORKER_FAILED"
    assert audit.parse_worker_output(text + "\n" + text, 0, 12)["audit_result"] == "WORKER_FAILED"
    assert audit.parse_worker_output(text, 0, 11)["audit_result"] == "WRONG_WORKER_GOAL"


@pytest.mark.parametrize("field,value", [
    ("search_status", "search_failed"), ("open_goals", 2),
    ("proven_steps", 0), ("source_precedes", False),
    ("web_key", "partial-proof"), ("web_partial", True),
    ("web_steps", 0), ("web_lines", 0),
    ("web_error", "UnverifiedProofTree"),
])
def test_completed_headline_cannot_bypass_search_or_web_gate(field: str, value: object) -> None:
    row = complete_row(12)
    row[field] = value
    assert not audit.qualified_complete(row, 12)


def test_all_33_fresh_rows_aggregate_without_prior_report() -> None:
    rows = [audit.parse_worker_output(audit.SENTINEL + json.dumps(complete_row(k)), 0, k)
            for k in audit.DOMAIN]
    assert audit.domain_counts(rows) == (33, 33, 0)
    rows[11]["audit_result"] = "PROOF_OR_WEB_NOT_VERIFIED"
    assert audit.domain_counts(rows) == (33, 32, 1)
    with pytest.raises(ValueError, match="duplicate"):
        audit.domain_counts(rows + [rows[-1]])


def test_preflight_refuses_unknown_tracked_modification(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for rel in (*audit.EXPECTED_BLOBS, *audit.EXPECTED_CHANGED, audit.R9_SOURCE):
        file = tmp_path / rel
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("fixture", encoding="utf-8")
    recorded = {
        ("branch", "--show-current"): audit.EXPECTED_BRANCH,
        ("rev-parse", "HEAD"): audit.EXPECTED_HEAD,
        ("diff", "--cached", "--name-only", "--"): "",
        ("diff", "--name-only", "HEAD", "--"): "",
    }
    for rel, blob in audit.EXPECTED_BLOBS.items():
        recorded[("rev-parse", f"HEAD:{rel}")] = blob
    monkeypatch.setattr(audit, "git", lambda _root, *args: recorded[args])
    monkeypatch.setattr(audit, "tracked_diff_digest", lambda _root: "test-sha")
    monkeypatch.setattr(audit, "checked_clause_position", lambda _root: 123)
    assert audit.preflight(tmp_path, check_remote=False)["tracked_diff_sha256"] == "test-sha"
    recorded[("diff", "--name-only", "HEAD", "--")] = ".pytest_cache/v/cache/nodeids"
    with pytest.raises(RuntimeError, match="expected clean tracked files"):
        audit.preflight(tmp_path, check_remote=False)



def test_preflight_rejects_old_head(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_git(_root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return audit.EXPECTED_BRANCH
        if args == ("rev-parse", "HEAD"):
            return "fdf60522b6d477209e9d8d67720a63f9863e419c"
        raise AssertionError(f"unexpected git call: {args}")
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="unreviewed branch or HEAD"):
        audit.preflight(tmp_path, check_remote=False)


def test_preflight_rejects_unreviewed_committed_blob(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for rel in audit.EXPECTED_BLOBS:
        file = tmp_path / rel
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("fixture", encoding="utf-8")
    recorded = {
        ("branch", "--show-current"): audit.EXPECTED_BRANCH,
        ("rev-parse", "HEAD"): audit.EXPECTED_HEAD,
        ("diff", "--cached", "--name-only", "--"): "",
        ("diff", "--name-only", "HEAD", "--"): "",
    }
    for rel, blob in audit.EXPECTED_BLOBS.items():
        recorded[("rev-parse", f"HEAD:{rel}")] = blob
    path = "phase170_r3_r9_toda712_cited_rewrite/source712.py"
    recorded[("rev-parse", f"HEAD:{path}")] = "deadbeef"
    monkeypatch.setattr(audit, "git", lambda _root, *args: recorded[args])
    with pytest.raises(RuntimeError, match="committed source changed"):
        audit.preflight(tmp_path, check_remote=False)


def test_source_clause_must_match_unique_reviewed_tex(tmp_path: Path) -> None:
    source = tmp_path / audit.R9_SOURCE
    source.parent.mkdir(parents=True)
    source.write_text("CLAUSE = " + repr(audit.EXPECTED_CLAUSE) + "\n", encoding="utf-8")
    tex = tmp_path / "sources/toda/Toda_07_2.tex"
    tex.parent.mkdir(parents=True)
    tex.write_text("pre" + audit.EXPECTED_CLAUSE + "post", encoding="utf-8")
    assert audit.checked_clause_position(tmp_path) == 3
    tex.write_text(audit.EXPECTED_CLAUSE + audit.EXPECTED_CLAUSE, encoding="utf-8")
    with pytest.raises(RuntimeError, match="ambiguous"):
        audit.checked_clause_position(tmp_path)


def test_worker_subprocess_explicitly_uses_utf8(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    recorded = {}

    def fake_run(cmd: list[str], **kwargs: object) -> SimpleNamespace:
        recorded["command"] = cmd
        recorded["environment"] = kwargs["env"]
        return SimpleNamespace(stdout=audit.SENTINEL + json.dumps(complete_row(12)) + "\n", returncode=0)

    monkeypatch.setattr(audit.subprocess, "run", fake_run)
    row = audit.run_worker(tmp_path, 12, 60, tmp_path)
    assert row["audit_result"] == "COMPLETE_AND_WEB_VERIFIED"
    assert recorded["command"][-2:] == ["--k", "12"]
    assert recorded["environment"]["PYTHONIOENCODING"] == "utf-8"
    assert (tmp_path / "k_012.log").exists()


def test_audit_runs_all_33_independently(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    snapshot = {"head": audit.EXPECTED_HEAD, "tracked_diff_sha256": "unchanged"}
    monkeypatch.setattr(audit, "preflight", lambda _root, check_remote=True: dict(snapshot))
    monkeypatch.setattr(audit, "explicit_n2_stems", lambda _path: tuple(range(34)))
    calls = []

    def worker(_root: Path, k: int, _timeout: int, _output: Path) -> dict:
        calls.append(k)
        return {**complete_row(k), "audit_result": "COMPLETE_AND_WEB_VERIFIED"}

    monkeypatch.setattr(audit, "run_worker", worker)
    assert audit.run(tmp_path, dry_run=False, timeout_seconds=10) == 0
    assert calls == list(audit.DOMAIN)
    paths = list((tmp_path / "EHPProofTracerRecovery").glob("phase170_r3_r10_n2_33_*/audit.json"))
    assert len(paths) == 1
    data = json.loads(paths[0].read_text(encoding="utf-8"))
    assert data["domain_checked"] == 33
    assert data["domain_complete"] == 33
    assert data["domain_gaps"] == 0
    assert data["tracked_unchanged"] is True
