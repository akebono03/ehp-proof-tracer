"""Offline guards for reviewed audit-only HEAD transitions."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


def audit_module():
    filename = Path(__file__).resolve().parents[1] / "audit.py"
    spec = importlib.util.spec_from_file_location("phase170_r3_r2_head_sync_contract", filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reviewed_stub(tmp_path: Path, *, branch: str = "develop", head: str | None = None,
                  extra: tuple[tuple[str, str], ...] = (),
                  missing: tuple[tuple[str, str], ...] = (),
                  source_blob: str = "reviewed", data_blob: str = "dbblob"):
    audit = audit_module()
    (tmp_path / "source.py").write_text("reviewed source\n", encoding="utf-8")
    (tmp_path / "data").mkdir(exist_ok=True)
    (tmp_path / "data" / "db.csv").write_text("n,k\n2,1\n", encoding="utf-8")
    changes = sorted((audit.REVIEWED_ADDED_AUDIT_FILES - set(missing)) | set(extra))
    encoded = b"".join((status + "\0" + path + "\0").encode("utf-8") for status, path in changes)
    calls = []

    def git(root, *args):
        calls.append(args)
        if args[:2] == ("diff", "--name-status"):
            return encoded
        if args[:2] == ("merge-base", "--is-ancestor"):
            return b""
        if args[:2] == ("diff", "--exit-code"):
            return b""
        if args[:3] == ("diff", "--cached", "--exit-code"):
            return b""
        raise AssertionError(f"unexpected git invocation: {args!r}")

    def git_text(root, *args):
        if args == ("branch", "--show-current"):
            return branch
        if args == ("rev-parse", "HEAD"):
            return audit.REVIEWED_HEAD if head is None else head
        if args == ("hash-object", "--", "source.py"):
            return source_blob
        if args == ("hash-object", "--", "data/db.csv"):
            return data_blob
        if args == ("rev-parse", "HEAD:data/db.csv"):
            return "dbblob"
        raise AssertionError(f"unexpected git text invocation: {args!r}")

    def parse_name_status_z(data: bytes):
        parts = data.decode("utf-8").split("\0")
        assert parts.pop() == ""
        return tuple((parts[i], parts[i + 1]) for i in range(0, len(parts), 2))

    return SimpleNamespace(
        git=git,
        git_text=git_text,
        parse_name_status_z=parse_name_status_z,
        REVIEWED_R2_HEAD="f9e9a9d59970943d967e2cbcb0a98f13b2471407",
        EXPECTED_BLOBS={"source.py": "reviewed"},
        DATA_FILES=("data/db.csv",),
        calls=calls,
    )


def test_actual_reviewed_audit_only_transition_accepted(tmp_path):
    audit = audit_module()
    reviewed = reviewed_stub(tmp_path)
    result = audit.preflight_after_reviewed_audit_commits(tmp_path, reviewed)
    assert result["head"] == audit.REVIEWED_HEAD
    assert len(result["allowed_added_committed_audit_files"]) == 19
    assert result["reviewed_blobs"] == {"source.py": "reviewed"}
    assert result["report_origin_head"] == audit.REVIEWED_R3_REPORT_HEAD
    assert ("merge-base", "--is-ancestor", reviewed.REVIEWED_R2_HEAD, audit.REVIEWED_HEAD) in reviewed.calls


@pytest.mark.parametrize("branch,head", [
    ("main", None),
    ("develop", "790db364a8531693572fc510f969da831f1f9ffb"),
    ("develop", "56347c34c36dd458d23af2851b7a1af531d00a6d"),
    ("develop", "1111111111111111111111111111111111111111"),
])
def test_unreviewed_branch_or_head_rejected(tmp_path, branch, head):
    audit = audit_module()
    with pytest.raises(RuntimeError, match="unreviewed branch or HEAD"):
        audit.preflight_after_reviewed_audit_commits(tmp_path, reviewed_stub(tmp_path, branch=branch, head=head))


def test_unexpected_production_modification_rejected(tmp_path):
    audit = audit_module()
    with pytest.raises(RuntimeError, match="unreviewed committed changes"):
        audit.preflight_after_reviewed_audit_commits(
            tmp_path, reviewed_stub(tmp_path, extra=(("M", "phase165_r52_r9_shared_math.py"),))
        )


def test_unexpected_added_audit_file_rejected(tmp_path):
    audit = audit_module()
    with pytest.raises(RuntimeError, match="unreviewed committed changes"):
        audit.preflight_after_reviewed_audit_commits(
            tmp_path, reviewed_stub(tmp_path, extra=(("A", "phase170_r3_r1_failure_frontier_audit/unknown.py"),))
        )


def test_missing_reviewed_audit_file_rejected(tmp_path):
    audit = audit_module()
    with pytest.raises(RuntimeError, match="unreviewed committed changes"):
        audit.preflight_after_reviewed_audit_commits(
            tmp_path, reviewed_stub(tmp_path, missing=(("A", "phase170_r3_r1_failure_frontier_audit/audit.py"),))
        )


def test_unreviewed_production_blob_rejected(tmp_path):
    audit = audit_module()
    with pytest.raises(RuntimeError, match="reviewed production changed"):
        audit.preflight_after_reviewed_audit_commits(
            tmp_path, reviewed_stub(tmp_path, source_blob="modified")
        )


def test_uncommitted_database_change_rejected(tmp_path):
    audit = audit_module()
    with pytest.raises(RuntimeError, match="uncommitted database edit"):
        audit.preflight_after_reviewed_audit_commits(
            tmp_path, reviewed_stub(tmp_path, data_blob="modified")
        )


def test_report_pre_commit_head_accepted_and_current_head_not_substituted(tmp_path):
    audit = audit_module()
    r3_path = tmp_path / "audit.json"
    r2_path = tmp_path / "r2" / "audit.json"
    r1_path = tmp_path / "r1" / "audit.json"
    r1_path.parent.mkdir()
    r2_path.parent.mkdir()
    label_rows = []
    r1_map = {}
    r2_map = {}
    for n, k in audit.TARGETS:
        label = f"pi_{n+k}^{n}"
        label_rows.append({
            "group": label,
            "search_status": "search_failed",
            "source_screen": {"typed_goal_count": 1},
            "r2_blocker_classification": "SOURCE_ORDER_OR_CITATION_DIAGNOSTIC",
            "r1_diagnostics_exact": ["unknown"],
        })
        r1_map[label] = {"diagnostics": ["unknown"]}
        r2_map[label] = {"blocker_classification": "SOURCE_ORDER_OR_CITATION_DIAGNOSTIC"}
    payload = {
        "phase": "170 R3-R1",
        "mode": "AUDIT_ONLY",
        "tracked_unchanged": True,
        "full_pytest_run": False,
        "review_required": False,
        "git": {"head": audit.REVIEWED_R3_REPORT_HEAD},
        "r1_report": str(r1_path),
        "r2_report": str(r2_path),
        "cases": label_rows,
    }
    r3_path.write_text(json.dumps(payload), encoding="utf-8")
    fake_r3 = SimpleNamespace(
        load_reports=lambda _root, _r2: ({}, {}, r1_map, r2_map, r1_path)
    )
    result = audit.check_reports(fake_r3, tmp_path, r3_path)
    assert len(result[3]) == 5
    payload["git"]["head"] = audit.REVIEWED_HEAD
    r3_path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(RuntimeError, match="not a reviewed"):
        audit.check_reports(fake_r3, tmp_path, r3_path)
