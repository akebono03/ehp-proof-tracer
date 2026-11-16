"""Fail-closed, no-production-import tests for Phase 175 R1 observational audit."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase175_r1_k4_audit import audit


def _csv(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "sphere.csv"
    path.write_text("k,n,id,orders,generator\n" + text, encoding="utf-8-sig")
    return path


def _six_rows() -> str:
    return (
        "4,2,0,4,eta2nu\n"
        "4,3,0,2,nueta\n"
        "4,4,0,2,nu4eta\n"
        "4,4,1,2,Enueta\n"
        "4,5,0,2,nu5eta\n"
        "4,6,0,0,0\n"
        "4,7,0,0,0\n"
    )


def _completed() -> dict[str, object]:
    return {
        "n": 4, "k": 4, "db_goal_typed": True,
        "search_status": "complete", "search_conclusion_matches_db": True,
        "search_open_count": 0, "search_proven_count": 5,
        "trust_verified": True, "model_root_verified": True,
        "web_key": "generic-complete-proof", "web_partial": False,
        "web_line_count": 11, "web_error": None,
    }


def test_registered_k4_scope_is_six_groups_not_seven_csv_summands(tmp_path: Path) -> None:
    path = _csv(tmp_path, _six_rows() + "4,,,,\n3,8,0,1,other\n")
    found = audit.registered_k4_rows(path)
    assert tuple(sorted(found)) == audit.EXPECTED_GROUPS
    assert len(found) == 6
    assert sum(map(len, found.values())) == 7
    assert [row["id"] for row in found[4, 4]] == ["0", "1"]


def test_registered_scope_rejects_missing_extra_and_duplicate_rows(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="REGISTERED_SCOPE_CHANGED"):
        audit.registered_k4_rows(_csv(tmp_path, _six_rows().replace("4,7,0,0,0\n", "")))
    with pytest.raises(RuntimeError, match="REGISTERED_SCOPE_CHANGED"):
        audit.registered_k4_rows(_csv(tmp_path, _six_rows() + "4,8,0,0,0\n"))
    with pytest.raises(ValueError, match="DUPLICATE_SUMMAND_ID"):
        audit.registered_k4_rows(_csv(tmp_path, _six_rows() + "4,4,1,2,repeat\n"))


def test_csv_validation_does_not_accept_ill_typed_k4_row(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="INVALID_COORDINATE"):
        audit.registered_k4_rows(_csv(tmp_path, _six_rows() + "4,wrong,0,0,0\n"))
    with pytest.raises(ValueError, match="CSV_HEADERS_CHANGED"):
        path = tmp_path / "missing.csv"
        path.write_text("k,n,id\n4,2,0\n", encoding="utf-8")
        audit.registered_k4_rows(path)


@pytest.mark.parametrize("change", [
    {"db_goal_typed": False},
    {"search_conclusion_matches_db": False},
    {"search_open_count": 1},
    {"search_proven_count": 0},
    {"trust_verified": False},
    {"model_root_verified": False},
    {"web_key": "generic-partial-proof"},
    {"web_partial": True},
    {"web_line_count": 0},
    {"web_error": "broken"},
])
def test_any_missing_proof_requirement_blocks_complete(change: dict[str, object]) -> None:
    row = _completed()
    row.update(change)
    assert audit.classify(row) != "COMPLETE_AND_WEB_VERIFIED"


def test_complete_trust_verified_result_is_accepted() -> None:
    assert audit.classify(_completed()) == "COMPLETE_AND_WEB_VERIFIED"


def test_named_generator_partial_remains_partial() -> None:
    row = {
        "db_goal_typed": True, "search_status": "search_failed",
        "search_conclusion_is_none": True, "search_open_count": 3,
        "web_key": "generic-partial-proof", "web_partial": True,
        "web_error": None, "abstract_certificate_present": True,
    }
    assert audit.classify(row) == "INCOMPLETE_AND_WEB_CONFIRMED"
    row["web_partial"] = False
    assert audit.classify(row) == "INCOMPLETE_WITH_DISCREPANCY"
    row["web_partial"] = True
    row["search_conclusion_is_none"] = False
    assert audit.classify(row) == "INCOMPLETE_WITH_DISCREPANCY"


def test_worker_output_requires_exact_one_json_marker() -> None:
    good = _completed()
    text = audit.WORKER_MARKER + json.dumps(good)
    assert audit.parse_worker_output(text, 0, 4, 4)["audit_result"] == "COMPLETE_AND_WEB_VERIFIED"
    assert audit.parse_worker_output(text + "\n" + text, 0, 4, 4)["audit_result"] == "WORKER_FAILED"
    assert audit.parse_worker_output(text, 4, 4, 4)["audit_result"] == "WORKER_FAILED"
    assert audit.parse_worker_output(text, 0, 4, 5)["audit_result"] == "WORKER_GOAL_MISMATCH"
    assert audit.parse_worker_output(audit.WORKER_MARKER + "bad", 0, 4, 4)["audit_result"] == "WORKER_JSON_INVALID"


def test_summary_distinguishes_incomplete_proofs_from_operational_problems() -> None:
    rows = [
        {"n": 4, "k": 4, "audit_result": "COMPLETE_AND_WEB_VERIFIED"},
        {"n": 3, "k": 4, "audit_result": "INCOMPLETE_AND_WEB_CONFIRMED"},
    ]
    totals = audit.summary(rows)
    assert totals["checked"] == 2
    assert totals["not_yet_checked"] == 4
    assert totals["complete"] == 1
    assert totals["unfinished"] == 1
    assert totals["execution_or_trust_failures"] == 0
    rows.append({"n": 5, "k": 4, "audit_result": "UNVERIFIED_COMPLETION"})
    assert audit.summary(rows)["execution_or_trust_failures"] == 1
    with pytest.raises(ValueError, match="DUPLICATE_WORKER_RESULT"):
        audit.summary(rows + [rows[0]])


def test_preflight_accepts_pinned_git_state_and_rejects_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed = {
        ("rev-parse", "--show-toplevel"): (0, str(tmp_path.resolve())),
        ("branch", "--show-current"): (0, "develop"),
        ("rev-parse", "HEAD"): (0, audit.REVIEWED_MAIN_MERGE),
        ("status", "--porcelain", "--untracked-files=no"): (0, ""),
        ("merge-base", "--is-ancestor", audit.REVIEWED_MAIN_MERGE, "HEAD"): (0, ""),
        ("rev-parse", "--verify", "origin/develop"): (0, "prior-dev"),
    }
    for name, blob in audit.SOURCE_BLOBS.items():
        observed[("rev-parse", "HEAD:" + name)] = (0, blob)
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("stub", encoding="utf-8")
    monkeypatch.setattr(audit, "git", lambda root, *args, **kwargs: observed[args])
    monkeypatch.setattr(audit, "registered_k4_rows", lambda path: {
        pair: [{"id": "0", "generator": "g", "orders": "2"}]
        for pair in audit.EXPECTED_GROUPS
    })
    result = audit.preflight(tmp_path)
    assert result["tracked_clean"] is True
    assert result["origin_develop_matches_head"] is False
    observed[("status", "--porcelain", "--untracked-files=no")] = (0, " M README.md")
    with pytest.raises(RuntimeError, match="TRACKED_OR_INDEX_CHANGES"):
        audit.preflight(tmp_path)
    observed[("status", "--porcelain", "--untracked-files=no")] = (0, "")
    observed[("rev-parse", "HEAD:data/sphere.csv")] = (0, "0" * 40)
    with pytest.raises(RuntimeError, match="SOURCE_PIN_MISMATCH"):
        audit.preflight(tmp_path)


def test_report_markdown_writes_six_rows_without_claiming_new_proof(tmp_path: Path) -> None:
    rows = []
    for n, k in audit.EXPECTED_GROUPS:
        rows.append({
            "n": n, "k": k,
            "registered_summands": [{"id": "0"}],
            "search_status": "search_failed", "search_open_count": 1,
            "search_proven_count": 0, "reference_count": 0,
            "web_key": "generic-partial-proof",
            "audit_result": "INCOMPLETE_AND_WEB_CONFIRMED",
        })
    payload = {"preflight": {"head": "a" * 40},
               "rows": rows, "summary": audit.summary(rows)}
    path = tmp_path / "report.md"
    audit.write_markdown(path, payload)
    markdown = path.read_text(encoding="utf-8")
    assert markdown.count("generic-partial-proof") == 6
    assert "全体 pytest は Phase 175 終了時" in markdown
    assert "新規証明ではない" in markdown


def test_dry_run_performs_no_proof_search_and_writes_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(audit, "preflight", lambda root: {
        "head": "a" * 40, "registered_summand_rows": 7,
    })
    monkeypatch.setattr(audit, "registered_k4_rows", lambda path: {
        pair: [{"id": "0"}] for pair in audit.EXPECTED_GROUPS
    })

    def no_worker(*args: object) -> dict[str, object]:
        raise AssertionError("DryRun must never launch search")

    monkeypatch.setattr(audit, "launch_worker", no_worker)
    assert audit.run(tmp_path, dry_run=True, timeout_seconds=12) == 0
    outputs = list(tmp_path.glob("EHPProofTracerAudit/phase175_r1_k4_audit/*/report.json"))
    assert len(outputs) == 1
    data = json.loads(outputs[0].read_text(encoding="utf-8"))
    assert data["result"] == "PASS_R1_READ_ONLY_DRYRUN"
    assert data["rows"] == []
    assert data["full_pytest_executed"] is False


def test_audit_preserves_proof_gaps_and_failure_exit_code(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(audit, "preflight", lambda root: {
        "head": "b" * 40, "registered_summand_rows": 7,
    })
    monkeypatch.setattr(audit, "registered_k4_rows", lambda path: {
        pair: [{"id": "0"}] for pair in audit.EXPECTED_GROUPS
    })
    monkeypatch.setattr(audit, "launch_worker", lambda root, n, k, seconds, directory: {
        "n": n, "k": k, "audit_result": (
            "INCOMPLETE_AND_WEB_CONFIRMED" if n != 7 else "WORKER_TIMEOUT"
        ),
        "search_status": "search_failed", "search_open_count": 1,
        "web_key": "generic-partial-proof",
    })
    assert audit.run(tmp_path, dry_run=False, timeout_seconds=1) == 2
    outputs = list(tmp_path.glob("EHPProofTracerAudit/phase175_r1_k4_audit/*/report.json"))
    assert len(outputs) == 1
    data = json.loads(outputs[0].read_text(encoding="utf-8"))
    assert data["result"] == "AUDIT_REQUIRES_INVESTIGATION"
    assert data["summary"]["unfinished"] == 5
    assert data["summary"]["execution_or_trust_failures"] == 1
    assert (outputs[0].parent / "report.md").is_file()
