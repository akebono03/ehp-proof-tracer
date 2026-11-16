"""Focused fail-closed R2 contracts using synthetic evidence only in tests."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace

import pytest

from phase175_r2_k4_frontier_audit import audit


def fixture_r1() -> dict[str, object]:
    """Test-only shape; never a fabricated production report."""
    rows = []
    for (n, k), status in audit.EXPECTED_STATUSES.items():
        incomplete = (n, k) in audit.OPEN_COUNTS
        if (n, k) in ((3, 4), (5, 4)):
            goals = [
                "CyclicStructureStatement(group=sample, generator=sample, order=2)",
                "Relation(lhs=sample, rhs=sample)",
                "Relation(lhs=sample, rhs=sample)",
            ]
        elif (n, k) == (6, 4):
            goals = [
                "MapSurjective(map=TodaDeltaMap(source_group=sample, target_group=sample))",
                "TodaPrimaryGroupZeroStatement(group=sample)",
            ]
        else:
            goals = []
        rows.append({
            "n": n, "k": k, "group": f"pi_{n+k}^{n}",
            "audit_result": status, "db_goal_typed": True,
            "search_status": "search_failed" if incomplete else "complete",
            "search_open_count": len(goals), "search_open_goals": goals,
            "search_proven_count": 0 if incomplete else 8,
            "search_conclusion_is_none": incomplete,
            "web_key": "generic-partial-proof" if incomplete else "generic-complete-proof",
            "web_partial": incomplete,
            "references": [],
            "search_diagnostics": ["no verified derivation"] if incomplete else [],
        })
    return {
        "phase": "175-R1", "mode": "READ_ONLY_AUDIT",
        "dry_run": False, "result": "PASS_R1_AUDIT_WITH_PROOF_GAPS",
        "tracked_unchanged": True,
        "production_changes": [], "new_given": 0,
        "new_mathematical_rules": 0, "full_pytest_executed": False,
        "preflight": {"tracked_clean": True, "branch": "develop", "head": "sample-head"},
        "summary": {"checked": 6, "complete": 3, "unfinished": 3,
                    "execution_or_trust_failures": 0},
        "rows": rows,
    }


def test_R1_six_group_contract_accepts_only_three_observed_gaps() -> None:
    found = audit.validate_r1(fixture_r1())
    assert [(row["n"], row["k"]) for row in found] == list(audit.UNFINISHED)
    assert [row["search_open_count"] for row in found] == [3, 3, 2]
    assert all(row["search_proven_count"] == 0 for row in found)


@pytest.mark.parametrize("field,value", [
    ("phase", "174-R74"),
    ("mode", "PROOF_PATCH"),
    ("dry_run", True),
    ("result", "PASS_R1_READ_ONLY_DRYRUN"),
    ("tracked_unchanged", False),
    ("production_changes", ["production.py"]),
    ("new_given", 1),
    ("new_mathematical_rules", 1),
    ("full_pytest_executed", True),
])
def test_reject_unreviewed_or_mutating_r1_report(field: str, value: object) -> None:
    report = fixture_r1()
    report[field] = value
    with pytest.raises(RuntimeError, match="EVIDENCE_CONTRACT_MISMATCH"):
        audit.validate_r1(report)


def test_r1_requires_full_exact_six_group_coverage() -> None:
    report = fixture_r1()
    report["rows"].pop()
    with pytest.raises(RuntimeError, match="SIX_ROWS_REQUIRED"):
        audit.validate_r1(report)
    report = fixture_r1()
    report["rows"].append(deepcopy(report["rows"][0]))
    with pytest.raises(RuntimeError, match="SIX_ROWS_REQUIRED"):
        audit.validate_r1(report)
    report = fixture_r1()
    report["rows"][0] = deepcopy(report["rows"][1])
    with pytest.raises(RuntimeError, match="DUPLICATE_OR_UNKNOWN_GROUP"):
        audit.validate_r1(report)


@pytest.mark.parametrize("pair,bad_status", [
    ((3, 4), "COMPLETE_AND_WEB_VERIFIED"),
    ((5, 4), "COMPLETE_AND_WEB_VERIFIED"),
    ((6, 4), "COMPLETE_AND_WEB_VERIFIED"),
    ((2, 4), "INCOMPLETE_AND_WEB_CONFIRMED"),
])
def test_never_promote_unknown_gap_to_complete(pair: tuple[int, int], bad_status: str) -> None:
    report = fixture_r1()
    target = next(row for row in report["rows"] if (row["n"], row["k"]) == pair)
    target["audit_result"] = bad_status
    with pytest.raises(RuntimeError, match="GROUP_STATUS_CHANGED"):
        audit.validate_r1(report)


def test_requires_type_checked_cyclic_root_obligations() -> None:
    report = fixture_r1()
    row = next(row for row in report["rows"] if row["n"] == 3)
    row["search_open_goals"][0] = "A claim typed only as prose"
    with pytest.raises(RuntimeError, match="CYCLIC_GOAL_MISSING"):
        audit.validate_r1(report)
    report = fixture_r1()
    row = next(row for row in report["rows"] if row["n"] == 5)
    row["search_open_goals"].pop()
    with pytest.raises(RuntimeError, match="UNFINISHED_EVIDENCE_CHANGED"):
        audit.validate_r1(report)


def test_requires_true_delta_surjectivity_obligation() -> None:
    report = fixture_r1()
    row = next(row for row in report["rows"] if row["n"] == 6)
    row["search_open_goals"][0] = "TodaDeltaMap(no surjectivity proof)"
    with pytest.raises(RuntimeError, match="DELTA_GOAL_MISSING"):
        audit.validate_r1(report)


def test_r1_summary_discrepancy_is_failure() -> None:
    report = fixture_r1()
    report["summary"]["complete"] = 6
    with pytest.raises(RuntimeError, match="COUNTS_CHANGED"):
        audit.validate_r1(report)


def test_choose_latest_valid_r1_without_selecting_dryrun(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    base = tmp_path / "EHPProofTracerAudit" / audit.R1_PACKAGE
    older = base / "20261111T074852_297718Z"
    newer = base / "20261111T075000_000000Z"
    older.mkdir(parents=True)
    newer.mkdir(parents=True)
    good = fixture_r1()
    (older / "report.json").write_text(json.dumps(good), encoding="utf-8")
    bad = deepcopy(good)
    bad["dry_run"] = True
    (newer / "report.json").write_text(json.dumps(bad), encoding="utf-8")
    assert audit.select_r1_report(tmp_path, None) == older / "report.json"
    assert audit.select_r1_report(tmp_path, older / "report.json") == (older / "report.json").resolve()
    with pytest.raises(RuntimeError, match="REPORT_NOT_FOUND"):
        audit.select_r1_report(tmp_path, tmp_path / "unknown.json")


def test_provenance_must_match_reviewed_source_pins() -> None:
    from phase175_r1_k4_audit.audit import SOURCE_BLOBS, REVIEWED_MAIN_MERGE

    report = fixture_r1()
    report["preflight"].update({
        "source_blobs": dict(SOURCE_BLOBS),
        "reviewed_phase174_main_merge": REVIEWED_MAIN_MERGE,
    })
    checked = {"head": "sample-head", "branch": "develop", "r1_pins": dict(SOURCE_BLOBS)}
    audit.verify_provenance(report, checked)
    report["preflight"]["head"] = "unreviewed-head"
    with pytest.raises(RuntimeError, match="SOURCE_LINEAGE_CHANGED"):
        audit.verify_provenance(report, checked)


def reviewed_provenance_fixture() -> tuple[dict[str, object], dict[str, object]]:
    """Use the actual R1 source pins, not invented mathematical source claims."""
    from phase175_r1_k4_audit.audit import SOURCE_BLOBS, REVIEWED_MAIN_MERGE

    report = fixture_r1()
    report["preflight"].update({
        "source_blobs": dict(SOURCE_BLOBS),
        "reviewed_phase174_main_merge": REVIEWED_MAIN_MERGE,
        "head": "4f87fc5722e85f7365250c07e684e959b71ae8bb",
    })
    checked = {
        "head": "b" * 40, "branch": "develop",
        "r1_pins": dict(SOURCE_BLOBS),
    }
    return report, checked


def test_post_r1_merge_accepts_only_added_r1_audit_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    report, checked = reviewed_provenance_fixture()
    paths = (
        "phase175_r1_k4_audit/audit.py",
        "phase175_r1_k4_audit/tests/test_audit.py",
    )
    changes = "\n".join("A\t" + path for path in paths)
    calls: list[tuple[str, ...]] = []

    def fake_git(root: Path, *args: str) -> str:
        assert root == tmp_path
        calls.append(args)
        return changes

    def fake_run(argv: list[str], **kwargs: object) -> SimpleNamespace:
        assert argv[:3] == ["git", "merge-base", "--is-ancestor"]
        assert argv[3:] == [report["preflight"]["head"], checked["head"]]
        assert kwargs["cwd"] == tmp_path
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(audit, "git", fake_git)
    monkeypatch.setattr(audit.subprocess, "run", fake_run)
    result = audit.verify_provenance(report, checked, root=tmp_path)
    assert result["mode"] == "AUDIT_ONLY_DESCENDANT"
    assert result["audit_only_added_paths"] == list(paths)
    assert len(calls) == 1
    assert calls[0][:3] == ("diff", "--name-status", "--no-renames")


@pytest.mark.parametrize("changed", [
    "M\tphase165_r52_r9_shared_math.py",
    "A\tphase175_r1_k4_audit/audit.py\nM\tweb_group_proof.py",
    "M\tphase175_r1_k4_audit/audit.py",
    "D\tphase175_r1_k4_audit/audit.py",
    "A\tphase175_r2_k4_frontier_audit/audit.py",
    "A\tREADME.md",
    "",
])
def test_post_r1_merge_rejects_other_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, changed: str,
) -> None:
    report, checked = reviewed_provenance_fixture()
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=0))
    monkeypatch.setattr(audit, "git", lambda *a: changed)
    with pytest.raises(RuntimeError, match="SOURCE_LINEAGE_CHANGED"):
        audit.verify_provenance(report, checked, root=tmp_path)


def test_post_r1_merge_rejects_unrelated_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    report, checked = reviewed_provenance_fixture()
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=1))
    monkeypatch.setattr(audit, "git", lambda *a: "A\tphase175_r1_k4_audit/audit.py")
    with pytest.raises(RuntimeError, match="not an ancestor"):
        audit.verify_provenance(report, checked, root=tmp_path)


def test_post_r1_merge_requires_real_sha_and_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    report, checked = reviewed_provenance_fixture()
    report["preflight"]["head"] = "not-a-git-sha"
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **kw: pytest.fail("must not run git"))
    with pytest.raises(RuntimeError, match="unverified different HEADs"):
        audit.verify_provenance(report, checked, root=tmp_path)
    report, checked = reviewed_provenance_fixture()
    with pytest.raises(RuntimeError, match="unverified different HEADs"):
        audit.verify_provenance(report, checked)


def test_same_head_needs_no_git_ancestry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report, checked = reviewed_provenance_fixture()
    checked["head"] = report["preflight"]["head"]
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **kw: pytest.fail("must not run git"))
    result = audit.verify_provenance(report, checked)
    assert result["mode"] == "SAME_HEAD"
    assert result["audit_only_added_paths"] == []


def test_post_r1_merge_rejects_source_pin_or_base_drift() -> None:
    report, checked = reviewed_provenance_fixture()
    report["preflight"]["source_blobs"]["data/sphere.csv"] = "unreviewed"
    with pytest.raises(RuntimeError, match="source pins or reviewed baseline"):
        audit.verify_provenance(report, checked)
    report, checked = reviewed_provenance_fixture()
    report["preflight"]["reviewed_phase174_main_merge"] = "unreviewed"
    with pytest.raises(RuntimeError, match="source pins or reviewed baseline"):
        audit.verify_provenance(report, checked)


def test_real_git_history_accepts_only_r1_audit_commit(tmp_path: Path) -> None:
    """Exercise actual merge-base and diff commands in a temporary repository."""
    def git_command(*args: str) -> str:
        cmd = subprocess.run(
            ["git", *args], cwd=tmp_path, text=True,
            capture_output=True, encoding="utf-8", check=True,
        )
        return cmd.stdout.strip()

    git_command("init", "-q")
    (tmp_path / "tracked_source.txt").write_text("unchanged source\n", encoding="utf-8")
    git_command("add", "tracked_source.txt")
    git_command("-c", "user.name=Audit Test", "-c", "user.email=audit@example.invalid",
                "commit", "-qm", "baseline")
    old_head = git_command("rev-parse", "HEAD")

    audit_dir = tmp_path / "phase175_r1_k4_audit"
    audit_dir.mkdir()
    (audit_dir / "audit.py").write_text("# read only audit\n", encoding="utf-8")
    git_command("add", "phase175_r1_k4_audit/audit.py")
    git_command("-c", "user.name=Audit Test", "-c", "user.email=audit@example.invalid",
                "commit", "-qm", "R1 audit added")
    merged_head = git_command("rev-parse", "HEAD")

    report, checked = reviewed_provenance_fixture()
    report["preflight"]["head"] = old_head
    checked["head"] = merged_head
    result = audit.verify_provenance(report, checked, root=tmp_path)
    assert result["mode"] == "AUDIT_ONLY_DESCENDANT"
    assert result["audit_only_added_paths"] == ["phase175_r1_k4_audit/audit.py"]

    (tmp_path / "tracked_source.txt").write_text("changed source\n", encoding="utf-8")
    git_command("add", "tracked_source.txt")
    git_command("-c", "user.name=Audit Test", "-c", "user.email=audit@example.invalid",
                "commit", "-qm", "unreviewed production edit")
    checked["head"] = git_command("rev-parse", "HEAD")
    with pytest.raises(RuntimeError, match="SOURCE_LINEAGE_CHANGED"):
        audit.verify_provenance(report, checked, root=tmp_path)


def test_preflight_pins_extra_dependencies_and_r1_preflight(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import phase175_r1_k4_audit.audit as r1_audit

    def fake_r1(_root: Path) -> dict[str, object]:
        return {"head": "reviewed", "branch": "develop", "tracked_clean": True,
                "source_blobs": {"a.py": "old"}, "origin_develop_matches_head": True}

    monkeypatch.setattr(r1_audit, "preflight", fake_r1)
    monkeypatch.setattr(audit, "git", lambda _root, *args: audit.EXTRA_PINS[args[1][5:]])
    for path in audit.EXTRA_PINS:
        f = tmp_path / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("source", encoding="utf-8")
    assert len(audit.preflight(tmp_path)["r2_extra_pins"]) == len(audit.EXTRA_PINS)
    next(iter(audit.EXTRA_PINS))
    changed = next(iter(audit.EXTRA_PINS))
    monkeypatch.setattr(audit, "git", lambda _root, *args: "unreviewed")
    with pytest.raises(RuntimeError, match="PIN_MISMATCH"):
        audit.preflight(tmp_path)
    monkeypatch.setattr(audit, "git", lambda _root, *args: audit.EXTRA_PINS[args[1][5:]])
    (tmp_path / changed).unlink()
    with pytest.raises(RuntimeError, match="SOURCE_MISSING"):
        audit.preflight(tmp_path)


def test_worker_fail_closed_on_missing_or_forged_marker(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(*args: object, **kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(returncode=0, stdout="no trusted marker", stderr="")

    monkeypatch.setattr(audit.subprocess, "run", fake_run)
    result = audit.launch_source_worker(tmp_path, 30, tmp_path)
    assert result["status"] == "SOURCE_WORKER_INVALID"
    assert (tmp_path / "source_worker.log").is_file()


def test_markdown_never_promotes_unproved_root(tmp_path: Path) -> None:
    record = {
        "preflight": {"head": "reviewed"}, "r1_report": "R1 report",
        "source_worker": {
            "data": {
                "pi_10_6": {
                    "screened_prior_sources_for_zero_goal": [
                        {"locator": "Proposition 5.8", "screened_count": 1},
                        {"locator": "(5.10)", "screened_count": 1},
                    ]
                }
            }
        },
    }
    path = tmp_path / "report.md"
    audit.write_markdown(path, record)
    text = path.read_text(encoding="utf-8")
    assert "EHP" in text
    assert "未解決" in text
    assert "ProofStep" in text
    assert "完成証明ではない" in text


def test_r2_only_writes_to_explicit_report_path(tmp_path: Path) -> None:
    report_path = tmp_path / "report.json"
    report = {"phase": "175-R2", "new_given": 0,
              "new_mathematical_rules": 0, "production_changes": []}
    audit.write_json(report_path, report)
    assert json.loads(report_path.read_text(encoding="utf-8")) == report
    assert list(tmp_path.iterdir()) == [report_path]
