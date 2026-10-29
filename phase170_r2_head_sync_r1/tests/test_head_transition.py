"""Head-transition tests: only the reviewed six-file R1 commit is admissible."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


def load_module():
    location = Path(__file__).resolve().parents[1] / "audit.py"
    spec = importlib.util.spec_from_file_location("r2_reviewed_r1_transition", location)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fake_git_for_r1(module, monkeypatch, *, modified_changes=None):
    expected = sorted(module.R1_COMMIT_ADDED_FILES)
    changes = [("A", name) for name in expected] if modified_changes is None else modified_changes
    encoded = b"".join((status + "\0" + filename + "\0").encode("utf-8")
                       for status, filename in changes)
    calls = []

    def fake_git(root, *args):
        calls.append(args)
        if args == ("merge-base", "--is-ancestor", module.R1_RECORDED_HEAD,
                    module.R1_COMMITTED_HEAD):
            return b""
        if args == ("diff", "--name-status", "-z", module.R1_RECORDED_HEAD,
                    module.R1_COMMITTED_HEAD):
            return encoded
        raise AssertionError(f"unexpected command: {args!r}")

    monkeypatch.setattr(module, "git", fake_git)
    return calls


def test_r1_only_commit_accepted_after_exact_git_check(monkeypatch, tmp_path):
    module = load_module()
    calls = fake_git_for_r1(module, monkeypatch)
    transition = module.reviewed_r1_head_transition(
        tmp_path, module.R1_RECORDED_HEAD, module.R1_COMMITTED_HEAD,
    )
    assert transition["kind"] == "REVIEWED_R1_ONLY_COMMIT"
    assert transition["added_files"] == sorted(module.R1_COMMIT_ADDED_FILES)
    assert len(calls) == 2


def test_same_reviewed_head_needs_no_diff(monkeypatch, tmp_path):
    module = load_module()
    monkeypatch.setattr(module, "git", lambda *args: pytest.fail("unexpected Git call"))
    result = module.reviewed_r1_head_transition(
        tmp_path, module.R1_COMMITTED_HEAD, module.R1_COMMITTED_HEAD,
    )
    assert result["kind"] == "SAME_HEAD"


def test_future_unreviewed_head_fails_closed(monkeypatch, tmp_path):
    module = load_module()
    monkeypatch.setattr(module, "git", lambda *args: pytest.fail("unexpected Git call"))
    with pytest.raises(RuntimeError, match="unreviewed R1 HEAD transition"):
        module.reviewed_r1_head_transition(
            tmp_path, module.R1_RECORDED_HEAD, "a" * 40,
        )


def test_extra_or_modified_production_path_rejected(monkeypatch, tmp_path):
    module = load_module()
    changes = [("A", name) for name in sorted(module.R1_COMMIT_ADDED_FILES)]
    changes.append(("M", "phase165_r52_r9_shared_math.py"))
    fake_git_for_r1(module, monkeypatch, modified_changes=changes)
    with pytest.raises(RuntimeError, match="unreviewed changes"):
        module.reviewed_r1_head_transition(
            tmp_path, module.R1_RECORDED_HEAD, module.R1_COMMITTED_HEAD,
        )


def test_missing_r1_path_rejected(monkeypatch, tmp_path):
    module = load_module()
    changes = [("A", name) for name in sorted(module.R1_COMMIT_ADDED_FILES)[:-1]]
    fake_git_for_r1(module, monkeypatch, modified_changes=changes)
    with pytest.raises(RuntimeError, match="unreviewed changes"):
        module.reviewed_r1_head_transition(
            tmp_path, module.R1_RECORDED_HEAD, module.R1_COMMITTED_HEAD,
        )


def test_invalid_r1_flags_not_accepted(monkeypatch, tmp_path):
    module = load_module()
    fake_git_for_r1(module, monkeypatch)
    data = {
        "phase": "170 R1", "mode": "AUDIT_ONLY", "scope": "sample",
        "git": {"head": module.R1_RECORDED_HEAD},
        "tracked_unchanged": False, "full_pytest_run": False,
        "cases": [{"group": f"pi_{n+k}^{n}"} for n, k in module.R1_GROUPS],
    }
    report = tmp_path / "audit.json"
    report.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(RuntimeError, match="protection flags"):
        module.load_r1(tmp_path, report, module.R1_COMMITTED_HEAD)


def test_valid_r1_report_and_six_paths_read_as_twelve_cases(monkeypatch, tmp_path):
    module = load_module()
    fake_git_for_r1(module, monkeypatch)
    data = {
        "phase": "170 R1", "mode": "AUDIT_ONLY", "scope": "sample",
        "git": {"head": module.R1_RECORDED_HEAD},
        "tracked_unchanged": True, "full_pytest_run": False,
        "cases": [{"group": f"pi_{n+k}^{n}"} for n, k in module.R1_GROUPS],
    }
    report = tmp_path / "audit.json"
    report.write_text(json.dumps(data), encoding="utf-8")
    actual, index, transition = module.load_r1(tmp_path, report, module.R1_COMMITTED_HEAD)
    assert actual == data
    assert len(index) == 12
    assert transition["kind"] == "REVIEWED_R1_ONLY_COMMIT"
