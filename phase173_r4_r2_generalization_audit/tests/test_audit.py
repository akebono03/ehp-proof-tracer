"""Offline focused tests for the read-only Phase 173 R4-R2 auditor."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import json

import pytest

from phase173_r4_r2_generalization_audit import audit


def test_frontier_selection_requires_registered_inputs() -> None:
    groups = tuple(sorted(set(audit.FRONTIER) | {(3, k) for k in range(4, 34)}))
    assert audit.select_targets(groups, "frontier") == audit.FRONTIER
    all_n3 = audit.select_targets(groups, "n3-all")
    assert len(all_n3) == 33
    assert all_n3[0] == (3, 4)
    assert all_n3[-1] == (4, 5)
    with pytest.raises(RuntimeError, match="frontier"):
        audit.select_targets(groups[1:], "frontier")
    with pytest.raises(ValueError, match="unknown scope"):
        audit.select_targets(groups, "unknown")


def test_scope_refuses_missing_k_even_if_frontier_is_complete() -> None:
    groups = tuple(sorted(set(audit.FRONTIER) | {(3, k) for k in range(8, 33)}))
    assert audit.select_targets(groups, "frontier") == audit.FRONTIER
    with pytest.raises(RuntimeError, match="registration differs"):
        audit.select_targets(groups, "n3-all")


def test_registered_pairs_read_real_n_and_k_columns(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text(
        "k,n,id\n-1,0,0\n0,1,0\n4,3,0\n4,3,1\n5,4,0\n5,2,0\n",
        encoding="utf-8-sig",
    )
    assert audit.registered_pairs(path) == ((3, 4), (4, 5))
    path.write_text("k,n,id\nbad,3,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed"):
        audit.registered_pairs(path)


def test_registered_pairs_skips_negative_stem_only_below_n3(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text(
        "k,n,id\n-1,0,0\n-2,1,0\n-1,2,0\n4,3,0\n",
        encoding="utf-8-sig",
    )
    assert audit.registered_pairs(path) == ((3, 4),)
    path.write_text("k,n,id\n-1,3,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed group coordinates at row 2"):
        audit.registered_pairs(path)


def test_registered_pairs_rejects_invalid_n3_coordinates(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("k,n,id\n4,broken,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed group coordinates at row 2"):
        audit.registered_pairs(path)
    path.write_text("k,n,id\n,3,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed group coordinates at row 2"):
        audit.registered_pairs(path)
    path.write_text("k,n\n4,3\n", encoding="utf-8")
    with pytest.raises(ValueError, match="sphere.csv lacks n, k, id"):
        audit.registered_pairs(path)


def test_parse_worker_never_claims_complete_from_partial_goal() -> None:
    row = {
        "n": 4, "k": 4, "search_status": "search_failed",
        "open_goals": 1, "proven_steps": 0,
        "root_matches_db_goal": True,
        "citation_model_verified": False,
        "web_key": "generic-partial-proof", "web_partial": True,
        "web_error": None, "audit_result": "COMPLETE_AND_WEB_VERIFIED",
    }
    result = audit.parse_worker_output(
        audit.SENTINEL + json.dumps(row), 0, 4, 4,
    )
    assert result["observation"] == "NOT_VERIFIED"
    assert result["open_goals"] == 1


def test_parse_worker_verified_result_requires_web_and_citations() -> None:
    row = {
        "n": 4, "k": 3, "db_goal_typed": True,
        "search_status": "complete", "search_complete": True,
        "root_matches_db_goal": True, "open_goals": 0, "proven_steps": 7,
        "citation_model_verified": True, "citation_count": 4,
        "web_key": "generic-complete-proof", "web_partial": False,
        "web_steps": 7, "web_lines": 9, "web_error": None,
    }
    complete = audit.parse_worker_output(audit.SENTINEL + json.dumps(row), 0, 4, 3)
    assert complete["observation"] == "COMPLETE_AND_WEB_VERIFIED"
    row["citation_model_verified"] = False
    incomplete = audit.parse_worker_output(audit.SENTINEL + json.dumps(row), 0, 4, 3)
    assert incomplete["observation"] == "NOT_VERIFIED"
    assert audit.parse_worker_output(audit.SENTINEL + json.dumps(row), 1, 4, 3)[
        "observation"
    ] == "WORKER_ERROR"


def test_parse_worker_rejects_wrong_or_malformed_outputs() -> None:
    assert audit.parse_worker_output("", 0, 3, 4)["observation"] == "WORKER_ERROR"
    assert audit.parse_worker_output(audit.SENTINEL + "{bad", 0, 3, 4)[
        "observation"
    ] == "INVALID_JSON"
    assert audit.parse_worker_output(
        audit.SENTINEL + json.dumps({"n": 3, "k": 5}), 0, 3, 4,
    )["observation"] == "WRONG_GROUP"


def test_preflight_refuses_wrong_head_or_tracked_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    responses = {
        ("rev-parse", "--show-toplevel"): str(tmp_path.resolve()),
        ("branch", "--show-current"): audit.BRANCH,
        ("rev-parse", "HEAD"): audit.REVIEWED_HEAD,
        ("status", "--porcelain", "--untracked-files=no"): "",
    }
    for file, blob in audit.REVIEWED_BLOBS.items():
        responses[("rev-parse", "HEAD:" + file)] = blob
        path = tmp_path / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture", encoding="utf-8")
    monkeypatch.setattr(audit, "git", lambda root, *args: responses[args])
    assert audit.preflight(tmp_path, check_remote=False)["head"] == audit.REVIEWED_HEAD
    responses[("rev-parse", "HEAD")] = "old-commit"
    with pytest.raises(RuntimeError, match="unreviewed checkout"):
        audit.preflight(tmp_path, check_remote=False)
    responses[("rev-parse", "HEAD")] = audit.REVIEWED_HEAD
    responses[("status", "--porcelain", "--untracked-files=no")] = " M README.md"
    with pytest.raises(RuntimeError, match="tracked/staged"):
        audit.preflight(tmp_path, check_remote=False)


def test_static_inference_scope_is_guarded(tmp_path: Path) -> None:
    values = {
        "phase165_r52_r9_shared_math.py":
            "if n == 4 and k == 3 and expansion_provider is None:\n",
        "phase168_r2_toda52_transport.py":
            "if n != 2 or dimension < 6:\nsource_n, source_k = 3, dimension - 3\n",
        "phase173_r4_r1_source_bound_56/rule.py":
            "and goal.lhs == TodaPrimaryGroup(7, 4)\n"
            "bridge, source_n=3, source_k=3, citing_assertion_id=citing_id\n",
        "phase173_r4_r1_public_connection/route.py":
            "registered_group_goal_candidates(bridge, n=4, k=3)\n",
    }
    for filename, contents in values.items():
        file = tmp_path / filename
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(contents, encoding="utf-8")
    static = audit.inspect_static(tmp_path)
    assert static["toda56_source_bound_root"] == "pi_7^4 only"
    (tmp_path / "phase168_r2_toda52_transport.py").write_text(
        "source_n, source_k = 3, dimension - 3", encoding="utf-8",
    )
    with pytest.raises(RuntimeError, match="Toda52 n2 guard"):
        audit.inspect_static(tmp_path)


def test_write_report_preserves_math_and_diagnostics_in_json(tmp_path: Path) -> None:
    report = {
        "scope": "frontier",
        "rows": [{"n": 4, "k": 4, "open_goals": 1,
                  "search_status": "search_failed", "web_key": "generic-partial-proof",
                  "observation": "NOT_VERIFIED", "diagnostics": ["未証明"]}],
    }
    audit.write_report(tmp_path, report)
    assert "$\\pi_{8}^{4}$" in (tmp_path / "audit.md").read_text(encoding="utf-8")
    assert json.loads((tmp_path / "audit.json").read_text(encoding="utf-8"))[
        "rows"
    ][0]["diagnostics"] == ["未証明"]


def test_run_refuses_to_certify_when_pi74_regresses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(
        audit, "preflight",
        lambda root, check_remote: {"head": audit.REVIEWED_HEAD,
                                    "remote_verified": check_remote},
    )
    monkeypatch.setattr(audit, "inspect_static", lambda root: {"scope": "reviewed"})
    monkeypatch.setattr(audit, "registered_pairs", lambda file: audit.FRONTIER)
    monkeypatch.setattr(
        audit, "run_worker",
        lambda root, n, k, timeout, output: {
            "n": n, "k": k, "observation": "NOT_VERIFIED",
            "search_status": "search_failed", "open_goals": 1,
        },
    )
    code = audit.run(tmp_path, dry_run=False, scope="frontier",
                     timeout=5, check_remote=False)
    assert code == 2
    outputs = list((tmp_path / "EHPProofTracerRecovery").glob("phase173_r4_r2_*"))
    assert len(outputs) == 1
    report = json.loads((outputs[0] / "audit.json").read_text(encoding="utf-8"))
    assert report["result"] == "PI74_REGRESSION_NOT_VERIFIED"
    assert report["pi74_regression_verified"] is False
    assert report["tracked_unchanged"] is True


def test_run_worker_uses_existing_public_worker_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed = {}
    row = {"n": 3, "k": 4, "search_status": "search_failed",
           "open_goals": 2, "web_key": "generic-partial-proof"}

    def fake_subprocess(command, **kwargs):
        observed["command"] = command
        observed["cwd"] = kwargs["cwd"]
        return SimpleNamespace(
            stdout=audit.SENTINEL + json.dumps(row), stderr="", returncode=0,
        )

    monkeypatch.setattr(audit.subprocess, "run", fake_subprocess)
    result = audit.run_worker(tmp_path, 3, 4, 5, tmp_path)
    assert observed["command"][2:4] == ["-m", "phase173_r1_nge3_audit.audit"]
    assert observed["command"][-4:] == ["--n", "3", "--k", "4"]
    assert observed["cwd"] == tmp_path
    assert result["observation"] == "NOT_VERIFIED"
    assert (tmp_path / "n_003_k_004.log").is_file()
