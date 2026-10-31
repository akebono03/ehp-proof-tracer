"""Focused offline contracts for the Phase 173 R1 read-only audit."""
from __future__ import annotations

from enum import Enum
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest

from phase173_r1_nge3_audit import audit


def verified_row(n: int, k: int) -> dict:
    return {
        "n": n, "k": k, "db_goal_typed": True,
        "search_status": "complete", "search_complete": True,
        "root_matches_db_goal": True, "open_goals": 0, "proven_steps": 2,
        "citation_model_verified": True, "citation_count": 1,
        "web_key": "generic-complete-proof", "web_partial": False,
        "web_steps": 2, "web_lines": 5, "web_error": None,
    }


def test_registered_groups_deduplicated_and_excludes_n2(tmp_path: Path) -> None:
    csv_path = tmp_path / "sphere.csv"
    csv_path.write_text(
        "k,n,id\n3,3,0\n3,3,1\n3,4,0\n3,5,0\n3,6,0\n3,7,0\n2,2,0\n0,65,0\n"
        ",,\n", encoding="utf-8-sig",
    )
    assert audit.registered_groups(csv_path) == (
        (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (65, 0),
    )


def test_invalid_registered_csv_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("k,n,id\nbad,3,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed k"):
        audit.registered_groups(path)
    path.write_text("k,n,id\n0,bad,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed n"):
        audit.registered_groups(path)
    path.write_text("k,n\n3,3\n", encoding="utf-8")
    with pytest.raises(ValueError, match="headers"):
        audit.registered_groups(path)


def test_priority_scope_has_38_and_all_scope_keeps_unselected() -> None:
    groups = tuple(sorted(
        {(3, k) for k in range(34)} | set(audit.PRIORITY_EXTRA) | {(9, 11)}
    ))
    selected = audit.select_groups(groups, "priority")
    assert len(selected) == 38
    assert (3, 3) in selected
    assert all(target in selected for target in audit.PRIORITY_EXTRA)
    assert audit.select_groups(groups, "all") == groups
    assert audit.summarize([], registered_count=len(groups), selected_count=len(selected))[
        "not_selected"
    ] == 1
    with pytest.raises(ValueError, match="unknown"):
        audit.select_groups(groups, "other")


def test_priority_scope_rejects_missing_targets_or_stems() -> None:
    groups = tuple(sorted({(3, k) for k in range(34)} | set(audit.PRIORITY_EXTRA)))
    with pytest.raises(RuntimeError, match="n=3"):
        audit.select_groups(groups[1:], "priority")
    without = tuple(pair for pair in groups if pair != (5, 3))
    with pytest.raises(RuntimeError, match="priority"):
        audit.select_groups(without, "priority")


@pytest.mark.parametrize("field,value,expected", [
    ("db_goal_typed", False, "DB_GOAL_UNTYPED_OR_MISSING"),
    ("search_status", "search_failed", "PROOF_UNFINISHED"),
    ("open_goals", 1, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("proven_steps", 0, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("root_matches_db_goal", False, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("citation_model_verified", False, "CITATION_MODEL_NOT_VERIFIED"),
    ("web_key", "generic-partial-proof", "WEB_NOT_VERIFIED"),
    ("web_partial", True, "WEB_NOT_VERIFIED"),
    ("web_lines", 0, "WEB_NOT_VERIFIED"),
    ("web_error", "TrustError", "WEB_NOT_VERIFIED"),
])
def test_classification_never_invents_complete_proof(
    field: str, value: object, expected: str,
) -> None:
    row = verified_row(3, 3)
    row[field] = value
    assert audit.classify_observation(row) == expected


def test_worker_exception_preempts_other_checks() -> None:
    assert audit.classify_observation({
        **verified_row(3, 3), "exception": "broken"
    }) == "WORKER_EXCEPTION"
    assert audit.classify_observation(verified_row(3, 3)) == "COMPLETE_AND_WEB_VERIFIED"


def test_parse_worker_reclassifies_untrusted_claims() -> None:
    row = {**verified_row(3, 3), "audit_result": "FAKE"}
    text = audit.SENTINEL + json.dumps(row)
    assert audit.parse_worker_output(text, 0, 3, 3)["audit_result"] == (
        "COMPLETE_AND_WEB_VERIFIED"
    )
    assert audit.parse_worker_output(text, 1, 3, 3)["audit_result"] == "WORKER_FAILED"
    assert audit.parse_worker_output(text + "\n" + text, 0, 3, 3)["audit_result"] == (
        "WORKER_FAILED"
    )
    assert audit.parse_worker_output(text, 0, 3, 4)["audit_result"] == "WRONG_WORKER_GOAL"
    assert audit.parse_worker_output(audit.SENTINEL + "bad", 0, 3, 3)[
        "audit_result"
    ] == "INVALID_WORKER_JSON"


def test_report_distinguishes_proof_gaps_from_worker_crashes() -> None:
    rows = [
        {**verified_row(3, 3), "audit_result": "COMPLETE_AND_WEB_VERIFIED"},
        {"n": 4, "k": 3, "audit_result": "PROOF_UNFINISHED"},
    ]
    summary = audit.summarize(rows, registered_count=797, selected_count=38)
    assert summary["checked"] == 2
    assert summary["complete"] == 1
    assert summary["incomplete_or_unverified"] == 1
    assert summary["not_selected"] == 759
    assert summary["not_checked_in_scope"] == 36
    assert summary["execution_failures"] == 0
    rows.append({"n": 5, "k": 3, "audit_result": "WORKER_EXCEPTION"})
    assert audit.summarize(rows, registered_count=797, selected_count=38)[
        "execution_failures"
    ] == 1
    with pytest.raises(ValueError, match="duplicate"):
        audit.summarize(rows + [rows[0]], registered_count=797, selected_count=38)


def test_preflight_rejects_dirty_tracked_files_and_wrong_head(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    responses = {
        ("rev-parse", "--show-toplevel"): str(tmp_path.resolve()),
        ("branch", "--show-current"): audit.BRANCH,
        ("rev-parse", "HEAD"): audit.REVIEWED_HEAD,
        ("status", "--porcelain", "--untracked-files=no"): "",
    }
    for filename, blob in audit.REVIEWED_BLOBS.items():
        responses[("rev-parse", "HEAD:" + filename)] = blob
        path = tmp_path / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture", encoding="utf-8")
    monkeypatch.setattr(audit, "git", lambda _root, *args: responses[args])
    monkeypatch.setattr(audit, "registered_groups", lambda _path: tuple((n, 0) for n in range(3, 800)))
    assert audit.preflight(tmp_path, check_remote=False)["head"] == audit.REVIEWED_HEAD
    responses[("status", "--porcelain", "--untracked-files=no")] = " M README.md"
    with pytest.raises(RuntimeError, match="tracked or staged"):
        audit.preflight(tmp_path, check_remote=False)
    responses[("status", "--porcelain", "--untracked-files=no")] = ""
    responses[("rev-parse", "HEAD")] = "another-head"
    with pytest.raises(RuntimeError, match="unreviewed checkout"):
        audit.preflight(tmp_path, check_remote=False)


def test_worker_uses_existing_apis_and_captures_model_references(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    class ProofSearchStatus(Enum):
        COMPLETE = "complete"

    def module(path: str, **objects: object) -> None:
        item = ModuleType(path)
        for key, value in objects.items():
            setattr(item, key, value)
        monkeypatch.setitem(sys.modules, path, item)

    goal = object()
    reference = SimpleNamespace(label="Toda Proposition", locator="(5.2)")
    given = SimpleNamespace(rule=SimpleNamespace(name="GIVEN"),
                            inference_rule=SimpleNamespace(literature_reference=reference))
    inferred = SimpleNamespace(rule=SimpleNamespace(name="INFERENCE"), inference_rule=None)
    result = SimpleNamespace(
        status=ProofSearchStatus.COMPLETE, conclusion=goal, references=("Toda",),
        proven_steps=(given, inferred), open_goals=(), diagnostics=(),
    )
    calls: list[tuple] = []

    def fake_search(*, n: int, k: int, bridge: object, context_sink):
        calls.append(("search", n, k))
        context_sink("screened")
        return result

    def fake_web(*, n: int, k: int, max_depth: int, mode: str, citation_source: str):
        calls.append(("web", n, k, max_depth, mode, citation_source))
        return SimpleNamespace(key="generic-complete-proof", partial_result=False,
                               steps=[1], rendered_lines=[1])

    model = SimpleNamespace(citations=(SimpleNamespace(
        number=1, reference=reference,
    ),))
    module("phase169_r10e4_ordered_db_prior.db_prior",
           exact_prior_database_result=lambda n, k: goal)
    module("phase165_r52_partial_proof", ProofSearchStatus=ProofSearchStatus)
    module("phase165_r52_r9_shared_math", build_shared_typed_bridge=lambda: "bridge")
    module("phase165_r55_nk_only_goal", search_group_from_registered_goal=fake_search)
    module("phase168_r3_4_link_bridge",
           build_linked_proof_narrative_model=lambda result, bridge: model)
    module("web_group_proof", build_standard_web_group_proof_view=fake_web)
    assert audit.worker(3, 3) == 0
    output = capsys.readouterr().out.strip()
    assert output.startswith(audit.SENTINEL)
    row = json.loads(output[len(audit.SENTINEL):])
    assert row["audit_result"] == "COMPLETE_AND_WEB_VERIFIED"
    assert row["citation_count"] == 1
    assert row["citations"] == [{"number": 1, "label": "Toda Proposition", "locator": "(5.2)"}]
    assert row["given_references"] == [{"label": "Toda Proposition", "locator": "(5.2)"}]
    assert calls == [("search", 3, 3), ("web", 3, 3, 2, "narrative", "model")]


def test_worker_does_not_promote_failed_search(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    class ProofSearchStatus(Enum):
        SEARCH_FAILED = "search_failed"
        COMPLETE = "complete"

    def module(path: str, **objects: object) -> None:
        item = ModuleType(path)
        for key, value in objects.items():
            setattr(item, key, value)
        monkeypatch.setitem(sys.modules, path, item)

    module("phase169_r10e4_ordered_db_prior.db_prior",
           exact_prior_database_result=lambda n, k: object())
    module("phase165_r52_partial_proof", ProofSearchStatus=ProofSearchStatus)
    module("phase165_r52_r9_shared_math", build_shared_typed_bridge=lambda: object())
    module("phase165_r55_nk_only_goal", search_group_from_registered_goal=lambda **kw:
           SimpleNamespace(status=ProofSearchStatus.SEARCH_FAILED,
                           conclusion=None, proven_steps=(), open_goals=("unsolved",),
                           diagnostics=("missing source",), references=()))
    module("web_group_proof", build_standard_web_group_proof_view=lambda **kw:
           SimpleNamespace(key="generic-partial-proof", partial_result=True,
                           steps=(), rendered_lines=()))
    assert audit.worker(4, 3) == 0
    line = capsys.readouterr().out.strip()
    row = json.loads(line[len(audit.SENTINEL):])
    assert row["search_status"] == "search_failed"
    assert row["open_goal_text"] == ["unsolved"]
    assert row["audit_result"] == "PROOF_UNFINISHED"


def test_dry_run_never_launches_a_worker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    all_groups = tuple(sorted({(3, k) for k in range(34)} | set(audit.PRIORITY_EXTRA)))
    monkeypatch.setattr(audit, "preflight", lambda root, check_remote: {"head": audit.REVIEWED_HEAD})
    monkeypatch.setattr(audit, "registered_groups", lambda _path: all_groups)
    monkeypatch.setattr(audit, "launch_worker", lambda *args: pytest.fail("worker launched"))
    assert audit.run(tmp_path, scope="priority", dry_run=True,
                     timeout_seconds=60, check_remote=False) == 0
    files = list((tmp_path / "EHPProofTracerRecovery").glob("phase173_r1_*/audit.json"))
    assert len(files) == 1
    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["summary"]["checked"] == 0
    assert data["summary"]["scope_total"] == 38
    assert data["result"] == "DRY_RUN_PASS"
    assert data["tracked_unchanged"] is True


def test_proof_gaps_allow_completed_audit_but_worker_failures_do_not(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    groups = ((3, 3), (4, 3))
    monkeypatch.setattr(audit, "preflight", lambda root, check_remote: {"head": audit.REVIEWED_HEAD})
    monkeypatch.setattr(audit, "registered_groups", lambda _path: groups)
    monkeypatch.setattr(audit, "launch_worker", lambda root, n, k, timeout_seconds, output:
                        {"n": n, "k": k, "audit_result": "PROOF_UNFINISHED"})
    assert audit.run(tmp_path, scope="all", dry_run=False,
                     timeout_seconds=30, check_remote=False) == 0
    report = list((tmp_path / "EHPProofTracerRecovery").glob("phase173_r1_*/audit.json"))
    data = json.loads(report[0].read_text(encoding="utf-8"))
    assert data["result"] == "AUDIT_COMPLETE_WITH_PROOF_GAPS"
    assert data["summary"]["incomplete_or_unverified"] == 2
    assert (report[0].parent / "audit.md").is_file()
    monkeypatch.setattr(audit, "launch_worker", lambda root, n, k, timeout_seconds, output:
                        {"n": n, "k": k, "audit_result": "WORKER_FAILED"})
    assert audit.run(tmp_path, scope="all", dry_run=False,
                     timeout_seconds=30, check_remote=False) == 2
