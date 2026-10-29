"""Focused audit-only contracts. No imported production application modules."""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase171_r1_n3_registered_audit import audit


def complete_row(k: int) -> dict:
    return {
        "n": 3, "k": k, "group_dimension": 3 + k,
        "db_goal_typed": True, "search_status": "complete",
        "root_matches_db_goal": True, "search_complete": True,
        "open_goals": 0, "proven_steps": 3,
        "web_key": "generic-complete-proof", "web_partial": False,
        "web_steps": 2, "web_lines": 3, "web_error": None,
    }


def test_registered_scope_includes_diagonal_and_all_stems() -> None:
    assert audit.N == 3
    assert audit.REGISTERED_K == tuple(range(34))
    assert audit.REGISTERED_K[0] == 0


def test_csv_deduplicates_generators_by_group_coordinates(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    body = "k,n,id,orders\n" + "".join(
        f"{k},3,0,2\n{k},3,1,2\n" for k in audit.REGISTERED_K
    )
    path.write_text(body + "33,2,0,2\n", encoding="utf-8-sig")
    assert audit.explicit_registered_stems(path) == audit.REGISTERED_K


def test_csv_missing_registered_group_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("k,n,id\n" + "".join(f"{k},3,0\n" for k in range(33)), encoding="utf-8")
    with pytest.raises(RuntimeError, match="missing=\\[33\\]"):
        audit.explicit_registered_stems(path)


def test_csv_extra_registered_group_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("k,n,id\n" + "".join(f"{k},3,0\n" for k in range(35)), encoding="utf-8")
    with pytest.raises(RuntimeError, match="unexpected=\\[34\\]"):
        audit.explicit_registered_stems(path)


def test_csv_rejects_malformed_k(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("k,n,id\nbad,3,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid registered"):
        audit.explicit_registered_stems(path)


@pytest.mark.parametrize("field,value,expected", [
    ("db_goal_typed", False, "DB_GOAL_UNTYPED_OR_MISSING"),
    ("search_status", "search_failed", "PROOF_UNFINISHED"),
    ("open_goals", 1, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("proven_steps", 0, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("root_matches_db_goal", False, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("search_complete", False, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("web_key", "generic-partial-proof", "WEB_NOT_VERIFIED"),
    ("web_partial", True, "WEB_NOT_VERIFIED"),
    ("web_steps", 0, "WEB_NOT_VERIFIED"),
    ("web_lines", 0, "WEB_NOT_VERIFIED"),
    ("web_error", "UnverifiedProofTree", "WEB_NOT_VERIFIED"),
])
def test_classification_checks_search_and_web(field: str, value: object, expected: str) -> None:
    row = complete_row(12)
    row[field] = value
    assert audit.classify_observation(row) == expected


def test_worker_exception_never_claims_completion() -> None:
    row = {**complete_row(11), "exception": "ValueError: invalid source"}
    assert audit.classify_observation(row) == "WORKER_EXCEPTION"


def test_complete_row_has_verified_status() -> None:
    assert audit.classify_observation(complete_row(12)) == "COMPLETE_AND_WEB_VERIFIED"


def test_parse_worker_output_valid_utf8_and_untrusted_classification() -> None:
    row = {**complete_row(12), "audit_result": "FAKED", "diagnostics": ["η₂"]}
    raw = audit.SENTINEL + json.dumps(row, ensure_ascii=False)
    result = audit.parse_worker_output(raw, 0, 12)
    assert result["audit_result"] == "COMPLETE_AND_WEB_VERIFIED"
    assert result["diagnostics"] == ["η₂"]
    row["search_status"] = "search_failed"
    result = audit.parse_worker_output(audit.SENTINEL + json.dumps(row), 0, 12)
    assert result["audit_result"] == "PROOF_UNFINISHED"


def test_parse_worker_output_rejects_failure_double_and_wrong_target() -> None:
    raw = audit.SENTINEL + json.dumps(complete_row(5))
    assert audit.parse_worker_output(raw, 1, 5)["audit_result"] == "WORKER_FAILED"
    assert audit.parse_worker_output(raw + "\n" + raw, 0, 5)["audit_result"] == "WORKER_FAILED"
    assert audit.parse_worker_output(raw, 0, 6)["audit_result"] == "WRONG_WORKER_GOAL"
    assert audit.parse_worker_output(audit.SENTINEL + "not json", 0, 5)["audit_result"] == "INVALID_WORKER_JSON"


def test_observational_gaps_not_counted_as_completed() -> None:
    rows = [dict(n=3, k=k, audit_result="COMPLETE_AND_WEB_VERIFIED") for k in range(34)]
    assert audit.summarize(rows)["complete"] == 34
    rows[12]["audit_result"] = "PROOF_UNFINISHED"
    summary = audit.summarize(rows)
    assert summary["checked"] == 34 and summary["complete"] == 33
    assert summary["gaps"] == 1 and summary["worker_failures"] == 0
    rows[1]["audit_result"] = "WORKER_EXCEPTION"
    assert audit.summarize(rows)["worker_failures"] == 1
    with pytest.raises(ValueError, match="duplicate"):
        audit.summarize(rows + [rows[0]])


def test_runner_forces_utf8_and_records_logs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    captured = {}
    def fake_run(cmd, **kw):
        captured["cmd"] = cmd
        captured["env"] = kw["env"]
        captured["timeout"] = kw["timeout"]
        return SimpleNamespace(returncode=0, stdout=audit.SENTINEL + json.dumps(
            {**complete_row(6), "note": "η₂"}, ensure_ascii=False) + "\n")
    monkeypatch.setattr(audit.subprocess, "run", fake_run)
    r = audit.launch_worker(tmp_path, tmp_path / "audit.py", 6, 120, tmp_path)
    assert r["audit_result"] == "COMPLETE_AND_WEB_VERIFIED"
    assert captured["env"]["PYTHONIOENCODING"] == "utf-8"
    assert captured["env"]["PYTHONUTF8"] == "1"
    assert captured["env"]["PYTHONDONTWRITEBYTECODE"] == "1"
    assert captured["cmd"][-2:] == ["--k", "6"]
    assert captured["timeout"] == 120
    assert (tmp_path / "k_006.log").read_text(encoding="utf-8").find("η₂") >= 0


def test_preflight_validates_commit_and_blobs_without_mutation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    answers = {
        ("branch", "--show-current"): audit.BRANCH,
        ("rev-parse", "HEAD"): audit.HEAD,
        ("diff", "--cached", "--name-only", "--"): "",
        ("diff", "--name-only", "HEAD", "--"): "",
    }
    for name, blob in audit.REVIEWED_BLOBS.items():
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("fixture", encoding="utf-8")
        answers[("rev-parse", "HEAD:" + name)] = blob
    monkeypatch.setattr(audit, "git", lambda _root, *args: answers[args])
    monkeypatch.setattr(audit, "tracked_state_digest", lambda _root: "sha-test")
    monkeypatch.setattr(audit, "explicit_registered_stems", lambda _path: audit.REGISTERED_K)
    before = audit.preflight(tmp_path, remote=False)
    assert before["registered_k"] == list(audit.REGISTERED_K)
    assert before["tracked_sha256"] == "sha-test"
    answers[("diff", "--name-only", "HEAD", "--")] = "web_group_proof.py"
    with pytest.raises(RuntimeError, match="tracked or staged"):
        audit.preflight(tmp_path, remote=False)


def test_preflight_rejects_commit_and_unreviewed_blob(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    answers = {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): "obsolete",
        ("diff", "--cached", "--name-only", "--"): "",
        ("diff", "--name-only", "HEAD", "--"): "",
    }
    monkeypatch.setattr(audit, "git", lambda _root, *args: answers[args])
    with pytest.raises(RuntimeError, match="unreviewed branch or HEAD"):
        audit.preflight(tmp_path, remote=False)
    answers[("rev-parse", "HEAD")] = audit.HEAD
    for name, blob in audit.REVIEWED_BLOBS.items():
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("fixture", encoding="utf-8")
        answers[("rev-parse", "HEAD:" + name)] = blob
    answers[("rev-parse", "HEAD:data/sphere.csv")] = "not-verified"
    with pytest.raises(RuntimeError, match="unreviewed tracked blob"):
        audit.preflight(tmp_path, remote=False)


def test_dry_run_validates_scope_without_running_workers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(audit, "preflight", lambda _root, remote: {"head": audit.HEAD})
    monkeypatch.setattr(audit, "launch_worker", lambda *args: pytest.fail("worker called in dry-run"))
    assert audit.run(tmp_path, dry_run=True, timeout_seconds=60, check_remote=False) == 0
    records = list((tmp_path / "EHPProofTracerRecovery").glob("phase171_r1_n3_audit_*/audit.json"))
    assert len(records) == 1
    report = json.loads(records[0].read_text(encoding="utf-8"))
    assert report["result"] == "DRY_RUN_PASS"
    assert report["tracked_unchanged"] is True


def test_full_audit_preserves_incomplete_observations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(audit, "preflight", lambda _root, remote: {"head": audit.HEAD})
    def fake_worker(root, script, k, timeout_seconds, output):
        return {"n": 3, "k": k, "search_status": "search_failed" if k == 12 else "complete",
                "audit_result": "PROOF_UNFINISHED" if k == 12 else "COMPLETE_AND_WEB_VERIFIED"}
    monkeypatch.setattr(audit, "launch_worker", fake_worker)
    assert audit.run(tmp_path, dry_run=False, timeout_seconds=60, check_remote=False) == 0
    files = list((tmp_path / "EHPProofTracerRecovery").glob("phase171_r1_n3_audit_*/audit.json"))
    assert len(files) == 1
    report = json.loads(files[0].read_text(encoding="utf-8"))
    assert report["summary"]["checked"] == 34
    assert report["summary"]["gaps"] == 1
    assert report["result"] == "AUDIT_COMPLETE_WITH_GAPS"
    assert (files[0].parent / "audit.md").is_file()


def test_worker_crash_requires_investigation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(audit, "preflight", lambda _root, remote: {"head": audit.HEAD})
    monkeypatch.setattr(audit, "launch_worker", lambda root, script, k, timeout_seconds, output: {
        "n": 3, "k": k,
        "audit_result": "WORKER_FAILED" if k == 1 else "COMPLETE_AND_WEB_VERIFIED",
    })
    assert audit.run(tmp_path, dry_run=False, timeout_seconds=60, check_remote=False) == 2
    files = list((tmp_path / "EHPProofTracerRecovery").glob("phase171_r1_n3_audit_*/audit.json"))
    assert len(files) == 1
    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["result"] == "AUDIT_COMPLETE_WITH_WORKER_FAILURES"


def test_worker_uses_real_api_shapes_and_collects_citations(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    import sys
    from enum import Enum
    from types import ModuleType

    class ProofSearchStatus(Enum):
        COMPLETE = "complete"

    def fake_module(path: str, **members: object) -> None:
        module = ModuleType(path)
        for key, value in members.items():
            setattr(module, key, value)
        monkeypatch.setitem(sys.modules, path, module)

    fixed_target = object()
    given = SimpleNamespace(rule=SimpleNamespace(name="GIVEN"),
        inference_rule=SimpleNamespace(literature_reference=SimpleNamespace(
            locator="Proposition 5.8", label="Toda Proposition 5.8")))
    inference = SimpleNamespace(rule=SimpleNamespace(name="INFERENCE"), inference_rule=None)
    proof_result = SimpleNamespace(
        status=ProofSearchStatus.COMPLETE, conclusion=fixed_target,
        proven_steps=[given, inference], open_goals=[], diagnostics=[],
    )
    calls = []

    def fake_search(*, n: int, k: int):
        calls.append(("search", n, k))
        return proof_result

    def fake_view(*, n: int, k: int, max_depth: int, mode: str, citation_source: str):
        calls.append(("web", n, k, max_depth, mode, citation_source))
        return SimpleNamespace(key="generic-complete-proof", partial_result=False,
                               steps=[object()], rendered_lines=[object()])

    fake_module("phase169_r10e4_ordered_db_prior.db_prior",
                exact_prior_database_result=lambda n, k: fixed_target)
    fake_module("phase165_r52_partial_proof", ProofSearchStatus=ProofSearchStatus)
    fake_module("phase165_r55_nk_only_goal", search_group_from_registered_goal=fake_search)
    fake_module("web_group_proof", build_standard_web_group_proof_view=fake_view)
    assert audit.worker(4) == 0
    text = capsys.readouterr().out.strip()
    assert text.startswith(audit.SENTINEL)
    row = json.loads(text[len(audit.SENTINEL):])
    assert row["audit_result"] == "COMPLETE_AND_WEB_VERIFIED"
    assert row["givens"] == [{"label": "Toda Proposition 5.8", "locator": "Proposition 5.8"}]
    assert row["inference_count"] == 1
    assert calls == [("search", 3, 4), ("web", 3, 4, 2, "narrative", "model")]


def test_worker_keeps_search_failures_observable(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    import sys
    from enum import Enum
    from types import ModuleType

    class ProofSearchStatus(Enum):
        SEARCH_FAILED = "search_failed"
        COMPLETE = "complete"

    def put(path: str, **members: object) -> None:
        item = ModuleType(path)
        for key, value in members.items():
            setattr(item, key, value)
        monkeypatch.setitem(sys.modules, path, item)

    target = object()
    put("phase169_r10e4_ordered_db_prior.db_prior",
        exact_prior_database_result=lambda n, k: target)
    put("phase165_r52_partial_proof", ProofSearchStatus=ProofSearchStatus)
    put("phase165_r55_nk_only_goal", search_group_from_registered_goal=lambda n, k: SimpleNamespace(
        status=ProofSearchStatus.SEARCH_FAILED, conclusion=None, proven_steps=[],
        open_goals=["typed missing claim"], diagnostics=["source not available"]
    ))
    put("web_group_proof", build_standard_web_group_proof_view=lambda **kwargs: SimpleNamespace(
        key="generic-partial-proof", partial_result=True, steps=[], rendered_lines=[]
    ))
    assert audit.worker(15) == 0
    text = capsys.readouterr().out.strip()
    row = json.loads(text[len(audit.SENTINEL):])
    assert row["audit_result"] == "PROOF_UNFINISHED"
    assert row["open_goals"] == 1
    assert row["open_goal_text"] == ["typed missing claim"]
    assert row["diagnostics"] == ["source not available"]
