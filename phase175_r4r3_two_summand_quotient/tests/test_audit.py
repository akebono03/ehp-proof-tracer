"""Isolated R4 observation-policy tests; fixtures are intentionally synthetic."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from phase175_r4r3_two_summand_quotient import audit


HEAD = "synthetic-verified-head"


def fixture_r4():
    return {
        "phase": "175-R4",
        "mode": "READ_ONLY_AUDIT",
        "gate": audit.REVIEWED_R4_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "full_pytest_executed": False,
        "production_changes": [],
        "preflight": {"head": HEAD, "pinned_source_count": 18},
        "observations": {
            "target_group": "pi_9^5",
            "prior_group": "pi_8^4",
            "open_goals_count": 3,
            "open_goals": ["CyclicStructureStatement(goal)", "Relation(a,b)", "Relation(b,a)"],
            "target_status": "INCOMPLETE_AND_WEB_CONFIRMED",
            "prior_status": "COMPLETE_AND_WEB_VERIFIED",
            "proof_complete": False,
        },
        "actual_rows": {
            "target": {"search_proven_count": 0},
            "prior_pi84": {"trust_verified": True},
        },
        "source": {
            "prior_pi84_printed": True,
            "source_proposition25": True,
            "source_ehp_delta_eta9": True,
            "source_ehp_delta_iota9": True,
            "source_pi95_quotient": True,
            "source_is_derived_goal_proof": False,
        },
    }


def test_passed_real_r4_report_is_still_unfinished() -> None:
    result = audit.validate_r4_report(fixture_r4(), HEAD)
    assert result == {
        "target_group": "pi_9^5",
        "prior_group": "pi_8^4",
        "open_goals_count": 3,
        "target_proven_steps": 0,
        "prior_verified": True,
        "source_prop25_seen": True,
        "proof_complete": False,
    }


@pytest.mark.parametrize("field,value", [
    ("phase", "175-R3"),
    ("mode", "PUBLIC_PROOF"),
    ("gate", "PASS_R4_AUDIT_ONLY_DRYRUN"),
    ("dry_run", True),
    ("new_given", 1),
    ("new_mathematical_rules", 1),
    ("full_pytest_executed", True),
    ("production_changes", ["phase165_r52_r9_shared_math.py"]),
])
def test_rejects_wrong_r4_policy(field: str, value: object) -> None:
    data = fixture_r4()
    data[field] = value
    with pytest.raises(RuntimeError, match="R4R3_R4_GATE_OR_POLICY_MISMATCH"):
        audit.validate_r4_report(data, HEAD)


@pytest.mark.parametrize("field,value", [
    ("head", "different-commit"),
    ("pinned_source_count", 17),
])
def test_rejects_r4_head_or_pins(field: str, value: object) -> None:
    data = fixture_r4()
    data["preflight"][field] = value
    with pytest.raises(RuntimeError, match="R4R3_R4_HEAD_OR_PINS_CHANGED"):
        audit.validate_r4_report(data, HEAD)


@pytest.mark.parametrize("section,field,value", [
    ("observations", "open_goals_count", 2),
    ("observations", "proof_complete", True),
    ("observations", "target_status", "COMPLETE_AND_WEB_VERIFIED"),
    ("observations", "prior_status", "INCOMPLETE_AND_WEB_CONFIRMED"),
    ("actual_rows.target", "search_proven_count", 1),
    ("actual_rows.prior_pi84", "trust_verified", False),
    ("source", "source_pi95_quotient", False),
    ("source", "source_is_derived_goal_proof", True),
])
def test_rejects_changed_mathematical_observation(
    section: str, field: str, value: object,
) -> None:
    data = deepcopy(fixture_r4())
    node = data
    for part in section.split("."):
        node = node[part]
    node[field] = value
    with pytest.raises(RuntimeError, match="R4R3_R4_OPEN_GOAL_OR_SOURCE_EVIDENCE_CHANGED"):
        audit.validate_r4_report(data, HEAD)


def test_latest_passed_r4_report_is_chosen(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    root = tmp_path / "EHPProofTracerAudit" / audit.R4_REPORT_FOLDER
    oldest = root / "20261117T020000Z"
    newest = root / "20261117T040000Z"
    oldest.mkdir(parents=True)
    newest.mkdir(parents=True)
    (oldest / "report.json").write_text(json.dumps(fixture_r4()), encoding="utf-8")
    failed = deepcopy(fixture_r4())
    failed["gate"] = "FAIL_R4_AUDIT_NOT_COMPLETED"
    (newest / "report.json").write_text(json.dumps(failed), encoding="utf-8")
    assert audit.r4_report_path() == oldest / "report.json"


def test_no_successful_r4_report_is_rejected(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    with pytest.raises(RuntimeError, match="R4R3_NO_PASSED_R4_REAL_REPORT"):
        audit.r4_report_path()


def test_explicit_report_path_is_not_silently_replaced(tmp_path: Path) -> None:
    expected = tmp_path / "report.json"
    expected.write_text(json.dumps(fixture_r4()), encoding="utf-8")
    assert audit.r4_report_path(expected) == expected.resolve()
    with pytest.raises(RuntimeError, match="R4R3_R4_REPORT_NOT_FOUND"):
        audit.r4_report_path(tmp_path / "missing.json")


def test_r4_same_head_lineage_needs_no_exception(monkeypatch, tmp_path: Path) -> None:
    def reject_git_calls(root, *args):
        raise AssertionError("same-HEAD report does not need Git transition")

    monkeypatch.setattr(audit, "git", reject_git_calls)
    found = audit.validate_r4_lineage(tmp_path, HEAD, HEAD)
    assert found["status"] == "SAME_HEAD"
    assert found["report_head"] == HEAD
    assert found["reviewed_changes"] == []


def reviewed_git_result(root: Path, *args: str) -> tuple[int, str]:
    if args == ("rev-parse", "HEAD"):
        return 0, audit.REVIEWED_R4_COMMIT
    if args == ("rev-parse", audit.REVIEWED_R4_COMMIT + "^1"):
        return 0, audit.REVIEWED_R4_REPORT_HEAD
    if args == (
        "diff", "--name-status", "--no-renames",
        audit.REVIEWED_R4_REPORT_HEAD, audit.REVIEWED_R4_COMMIT,
    ):
        return 0, "\n".join(
            "\t".join((status, path))
            for path, status in audit.REVIEWED_R4_COMMIT_CHANGES.items()
        )
    raise AssertionError(f"unexpected Git command: {args!r}")


def test_r4_reviewed_one_commit_is_accepted(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "git", reviewed_git_result)
    found = audit.validate_r4_lineage(
        tmp_path, audit.REVIEWED_R4_REPORT_HEAD, audit.REVIEWED_R4_COMMIT,
    )
    assert found["status"] == "REVIEWED_R4_AUDIT_ONLY_COMMIT"
    assert found["current_head"] == audit.REVIEWED_R4_COMMIT
    assert len(found["reviewed_changes"]) == 9
    sample = fixture_r4()
    sample["preflight"]["head"] = found["report_head"]
    assert audit.validate_r4_report(sample, found["report_head"])["proof_complete"] is False


@pytest.mark.parametrize("reported,current", [
    ("unreviewed-report", audit.REVIEWED_R4_COMMIT),
    (audit.REVIEWED_R4_REPORT_HEAD, "unreviewed-next-commit"),
    (audit.REVIEWED_R4_COMMIT, audit.REVIEWED_R4_REPORT_HEAD),
])
def test_r4_unreviewed_head_transitions_are_rejected(
    monkeypatch, tmp_path: Path, reported: str, current: str,
) -> None:
    monkeypatch.setattr(audit, "git", reviewed_git_result)
    with pytest.raises(RuntimeError, match="UNREVIEWED_HEAD_TRANSITION"):
        audit.validate_r4_lineage(tmp_path, reported, current)


def test_r4_commit_with_wrong_parent_is_rejected(monkeypatch, tmp_path: Path) -> None:
    def wrong_parent(root, *args):
        if args == ("rev-parse", audit.REVIEWED_R4_COMMIT + "^1"):
            return 0, "different-parent"
        return reviewed_git_result(root, *args)

    monkeypatch.setattr(audit, "git", wrong_parent)
    with pytest.raises(RuntimeError, match="UNREVIEWED_PARENT"):
        audit.validate_r4_lineage(
            tmp_path, audit.REVIEWED_R4_REPORT_HEAD, audit.REVIEWED_R4_COMMIT,
        )


def test_r4_commit_with_wrong_live_head_is_rejected(monkeypatch, tmp_path: Path) -> None:
    def wrong_head(root, *args):
        if args == ("rev-parse", "HEAD"):
            return 0, "different-head"
        return reviewed_git_result(root, *args)

    monkeypatch.setattr(audit, "git", wrong_head)
    with pytest.raises(RuntimeError, match="CURRENT_HEAD_MISMATCH"):
        audit.validate_r4_lineage(
            tmp_path, audit.REVIEWED_R4_REPORT_HEAD, audit.REVIEWED_R4_COMMIT,
        )


@pytest.mark.parametrize("changed", [
    {"phase165_r52_r9_shared_math.py": "M"},
    {"phase175_r4_pi95_audit/audit.py": "M"},
    {"phase175_r4_pi95_audit/README.md": "D"},
    {"phase175_r4_pi95_audit/audit.py": "A", "extra.py": "A"},
    {},
])
def test_r4_commit_with_unreviewed_diff_is_rejected(
    monkeypatch, tmp_path: Path, changed: dict[str, str],
) -> None:
    def altered_diff(root, *args):
        if args and args[0] == "diff":
            return 0, "\n".join(f"{status}\t{path}" for path, status in changed.items())
        return reviewed_git_result(root, *args)

    monkeypatch.setattr(audit, "git", altered_diff)
    with pytest.raises(RuntimeError, match="UNREVIEWED_COMMIT_DIFF"):
        audit.validate_r4_lineage(
            tmp_path, audit.REVIEWED_R4_REPORT_HEAD, audit.REVIEWED_R4_COMMIT,
        )


def test_r4_lineage_rejects_missing_head(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "git", reviewed_git_result)
    with pytest.raises(RuntimeError, match="HEAD_OR_PINS_CHANGED"):
        audit.validate_r4_lineage(tmp_path, None, audit.REVIEWED_R4_COMMIT)
