"""Focused tests of read-only Git-environment helpers."""
from pathlib import Path

from phase169_git_environment_readonly_audit.audit import (
    conflict_copy_files, longest_audit_files, markdown_report,
)


def test_conflict_files_found_in_refs_and_logs(tmp_path: Path):
    repo = tmp_path / "repo"
    refs = repo / ".git" / "refs" / "heads"
    logs = repo / ".git" / "logs" / "refs" / "heads"
    refs.mkdir(parents=True)
    logs.mkdir(parents=True)
    (refs / "develop (oomae-pc11 の競合コピー 2026-10-28)").write_text("deadbeef\n", encoding="utf-8")
    (logs / "develop (conflicted copy 2026-10-28)").write_text("reflog\n", encoding="utf-8")
    rows = conflict_copy_files(repo)
    assert len(rows) == 2
    assert rows[0]["path"].startswith(".git/")
    assert rows[1]["path"].startswith(".git/")
    assert (refs / "develop (oomae-pc11 の競合コピー 2026-10-28)").exists()


def test_long_files_sorted_without_modifying(tmp_path: Path):
    repo = tmp_path / "repo"
    base = repo / "phase169_r10et_r5d_staged_audit_guard" / "output" / "run"
    base.mkdir(parents=True)
    short = base / "short.py"
    long = base / ("long_" + "x" * 120 + ".py")
    short.write_text("x", encoding="utf-8")
    long.write_text("x", encoding="utf-8")
    rows = longest_audit_files(repo)
    assert len(rows) == 2
    assert rows[0]["path"].endswith(long.name)
    assert rows[0]["absolute_path_length"] > rows[1]["absolute_path_length"]
    assert short.exists() and long.exists()


def test_empty_conflicts_and_missing_output(tmp_path: Path):
    (tmp_path / ".git").mkdir()
    assert conflict_copy_files(tmp_path) == []
    assert longest_audit_files(tmp_path) == []


def test_markdown_report_japanese():
    commands = {name: {"exit_code": 0, "stdout": "ok", "stderr": ""}
                for name in ("version", "head", "branch")}
    report = markdown_report({"root": "C:/repo", "recorded_at": "2026-10-28",
                              "git": commands, "dropbox_conflict_copies": [],
                              "long_generated_paths": []})
    assert "読み取り専用" in report
    assert "ステージ領域" in report
