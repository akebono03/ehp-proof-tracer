"""R3B regression checks for R1 Gate report commit ancestry and fail-closed behavior."""
import importlib.util
import json
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "run.py"
SPEC = importlib.util.spec_from_file_location("phase169_r3b_closeout", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def make_gate_report(recovery: Path, head: str) -> Path:
    directory = recovery / "phase169_closeout_r1_20261028_193510_755227"
    directory.mkdir(parents=True)
    focused_log = directory / "focused_pytest.log"
    active_log = directory / "active_full_pytest.log"
    focused_log.write_text("67 passed in 21.86s\n", encoding="utf-8")
    active_log.write_text("3546 passed in 34.95s\n", encoding="utf-8")
    report = {
        "mode": "PHASE169_END_OF_PHASE_TEST",
        "head": head,
        "reviewed_files": 13,
        "r6_cases": 19,
        "git_index_preserved": True,
        "phase169_certified": False,
        "phase169_test_gate_pass": True,
        "decision": "TEST_GATE_PASS_PENDING_PHASE169_CLOSEOUT_DOCUMENTATION",
        "focused": {
            "passed_count": 67,
            "exit_code": 0,
            "log": str(focused_log),
            "command": ["python", "-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings", "-p", "no:cacheprovider", "focused.py"],
        },
        "active_full": {
            "passed_count": 3546,
            "exit_code": 0,
            "log": str(active_log),
            "command": ["python", "-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings", "-p", "no:cacheprovider", "tests"],
        },
    }
    path = directory / "report.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    return path


def mock_reviewed_history(monkeypatch, head: str) -> None:
    def fake_git(_root: Path, *args: str) -> str:
        if args == ("merge-base", MODULE.BASELINE_HEAD, head):
            return MODULE.BASELINE_HEAD
        if args == ("merge-base", head, MODULE.REVIEWED_REMOTE_HEAD):
            return head
        raise AssertionError("Unexpected Git query: " + repr(args))

    monkeypatch.setattr(MODULE, "git", fake_git)


def test_intermediate_reviewed_commit_accepted(tmp_path: Path, monkeypatch) -> None:
    head = "a" * 40
    path = make_gate_report(tmp_path, head)
    mock_reviewed_history(monkeypatch, head)
    result_path, report = MODULE.inspect_report(tmp_path, tmp_path / "repo")
    assert result_path == path
    assert report["head"] == head
    assert report["focused"]["passed_count"] == 67
    assert report["active_full"]["passed_count"] == 3546


@pytest.mark.parametrize("head", [
    MODULE.BASELINE_HEAD,
    MODULE.REVIEWED_REMOTE_HEAD,
])
def test_reviewed_range_endpoints_accepted(tmp_path: Path, monkeypatch, head: str) -> None:
    path = make_gate_report(tmp_path, head)
    mock_reviewed_history(monkeypatch, head)
    result_path, report = MODULE.inspect_report(tmp_path, tmp_path / "repo")
    assert result_path == path
    assert report["head"] == head


def test_unrelated_commit_rejected(tmp_path: Path, monkeypatch) -> None:
    head = "b" * 40
    make_gate_report(tmp_path, head)

    def fake_git(_root: Path, *args: str) -> str:
        if args == ("merge-base", MODULE.BASELINE_HEAD, head):
            return "c" * 40
        raise AssertionError("Unexpected Git query: " + repr(args))

    monkeypatch.setattr(MODULE, "git", fake_git)
    with pytest.raises(RuntimeError, match="outside reviewed commit ancestry"):
        MODULE.inspect_report(tmp_path, tmp_path / "repo")


def test_failed_test_report_rejected(tmp_path: Path, monkeypatch) -> None:
    head = "a" * 40
    path = make_gate_report(tmp_path, head)
    data = json.loads(path.read_text(encoding="utf-8"))
    data["active_full"]["exit_code"] = 1
    path.write_text(json.dumps(data), encoding="utf-8")
    mock_reviewed_history(monkeypatch, head)
    with pytest.raises(RuntimeError, match="results or command differ"):
        MODULE.inspect_report(tmp_path, tmp_path / "repo")


def test_missing_test_log_rejected(tmp_path: Path, monkeypatch) -> None:
    head = "a" * 40
    path = make_gate_report(tmp_path, head)
    data = json.loads(path.read_text(encoding="utf-8"))
    Path(data["focused"]["log"]).unlink()
    mock_reviewed_history(monkeypatch, head)
    with pytest.raises(RuntimeError, match="pytest log missing"):
        MODULE.inspect_report(tmp_path, tmp_path / "repo")


def test_missing_report_is_diagnosed(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="No R1 Gate report.json found"):
        MODULE.inspect_report(tmp_path, tmp_path / "repo")
