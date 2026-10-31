"""Isolated tests for Phase 171 final gate; full active pytest is never run here."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import re
import subprocess
from types import SimpleNamespace
import zipfile

import pytest

from phase171_closeout_r3_phase_end_gate import closeout as c


def test_active_command_runs_exactly_the_reviewed_active_tests():
    assert c.ACTIVE_ARGS == (
        "-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings",
        "-p", "no:cacheprovider", "tests",
    )


@pytest.mark.parametrize("output,code", [
    ("3546 passed in 34.94s\n", 0),
    ("================ 3546 passed in 34.94s ================\n", 0),
    ("3600 passed, 3 skipped in 51.2s\n", 0),
])
def test_pytest_pass_count_accepts_valid_summaries(output, code):
    count, summary = c.pytest_pass_count(output, code)
    assert count >= 3546
    assert "passed" in summary


@pytest.mark.parametrize("output,code", [
    ("3546 passed in 34.94s\n", 1),
    ("1 failed, 3546 passed in 34.94s\n", 0),
    ("no tests ran in 0.2s\n", 0),
    ("0 passed in 0.2s\n", 0),
    ("100 errors, 3546 passed\n", 0),
])
def test_pytest_pass_count_refuses_false_completion(output, code):
    with pytest.raises(RuntimeError):
        c.pytest_pass_count(output, code)


def test_five_language_appropriate_final_sections():
    sections = c.closure_sections(3551, "3551 passed in 29.4s")
    assert set(sections) == set(c.BASE_DOC_BLOBS)
    assert "Current status — Phase 171 closed" in sections["README.md"]
    assert "Phase 171 正式終了" in sections["docs/development_log.md"]
    for path, value in sections.items():
        assert value.count(c.FINAL_MARKER) == 1
        assert "3551 passed" in value
        assert "Phase 171" in value
        assert "pytest" in value
        if path != "README.md":
            assert "正式終了" in value or "終了" in value


def fake_before_docs() -> dict[str, bytes]:
    docs = {}
    for relative in c.BASE_DOC_BLOBS:
        if relative == "README.md":
            docs[relative] = (
                "# EHP Proof Tracer\n\n<!-- " + c.R2_MARKER + " -->\n\n"
                "## Phase 171 — pending\n\n# Phase 170 record\n"
            ).encode("utf-8")
        elif relative == "docs/design.md":
            docs[relative] = ("# Original\r\r\n\r\nHistory.\r\r\n\r\n## Phase 171 pending\r\n").encode("utf-8")
        else:
            docs[relative] = ("# 過去の本文\n\n## Phase 171 pending\n").encode("utf-8")
    return docs


def test_final_documents_preserve_every_historical_byte():
    before = fake_before_docs()
    sections = c.closure_sections(3563, "3563 passed in 55.3s")
    output = c.closure_documents(before, sections)
    assert set(output) == set(before)
    for path, original in before.items():
        updated = output[path]
        assert updated != original
        assert updated.count(c.FINAL_MARKER.encode("ascii")) == 1
        if path == "README.md":
            assert updated.startswith(b"# EHP Proof Tracer\n\n")
            index = updated.index(("<!-- " + c.R2_MARKER).encode("ascii"))
            assert updated[index:] == original[len(b"# EHP Proof Tracer\n\n"):]
        else:
            assert updated.startswith(original)
    assert b"History.\r\r\n" in output["docs/design.md"]
    assert b"\r\n<!-- " + c.FINAL_MARKER.encode("ascii") in output["docs/design.md"]


def test_second_final_update_refused():
    before = fake_before_docs()
    sections = c.closure_sections(3555, "3555 passed in 12.1s")
    first = c.closure_documents(before, sections)
    with pytest.raises(ValueError, match="already exists"):
        c.closure_documents(first, sections)


def test_missing_document_refused():
    before = fake_before_docs()
    before.pop("docs/design.md")
    with pytest.raises(ValueError, match="five"):
        c.closure_documents(before, c.closure_sections(1, "1 passed"))


def test_readme_marker_missing_refused():
    before = fake_before_docs()
    before["README.md"] = b"# README\n"
    with pytest.raises(ValueError, match="R2 marker"):
        c.closure_documents(before, c.closure_sections(1, "1 passed"))


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True,
                          text=True, encoding="utf-8")
    return proc.stdout.strip()


class FakeR2:
    @staticmethod
    def lf_text(data: bytes) -> str:
        return re.sub(r"\r+\n", "\n", data.decode("utf-8-sig"))

    @staticmethod
    def updated_document(path: str, original: bytes) -> bytes:
        if path == "README.md":
            return original.replace(b"# EHP Proof Tracer\n\n", (
                "# EHP Proof Tracer\n\n<!-- " + c.R2_MARKER + " -->\n\n"
            ).encode("utf-8"), 1)
        return original + b"\n## Phase 171 pending\n"


@pytest.fixture
def reviewed_repo(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    bare = tmp_path / "origin.git"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)
    subprocess.run(["git", "init", "-q", "-b", "develop", str(root)], check=True)
    git(root, "config", "user.name", "test")
    git(root, "config", "user.email", "test@example.invalid")
    for path in c.BASE_DOC_BLOBS:
        file = root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(
            b"# EHP Proof Tracer\n\n# Prior history\n" if path == "README.md"
            else b"# Past\n\nHistory\n"
        )
    for path in c.SOURCE_BLOBS:
        file = root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(b"# reviewed source\n")
    (root / "tests").mkdir()
    git(root, "add", ".")
    git(root, "commit", "-qm", "reviewed baseline")
    baseline = git(root, "rev-parse", "HEAD")
    git(root, "remote", "add", "origin", str(bare))
    git(root, "push", "-q", "-u", "origin", "develop")
    monkeypatch.setattr(c, "REVIEWED_HEAD", baseline)
    monkeypatch.setattr(c, "SOURCE_BLOBS", {
        path: git(root, "rev-parse", "HEAD:" + path) for path in c.SOURCE_BLOBS
    })
    monkeypatch.setattr(c, "BASE_DOC_BLOBS", {
        path: git(root, "rev-parse", "HEAD:" + path) for path in c.BASE_DOC_BLOBS
    })
    monkeypatch.setattr(c, "load_r2_writer", lambda root: FakeR2)
    for path in c.BASE_DOC_BLOBS:
        file = root / path
        file.write_bytes(FakeR2.updated_document(path, file.read_bytes()))
    return root


def test_preflight_allows_exactly_the_five_r2_documents(reviewed_repo):
    audit = c.preflight(reviewed_repo)
    assert set(audit["tracked_before"]) == set(c.BASE_DOC_BLOBS)
    assert audit["head"] == c.REVIEWED_HEAD
    assert all(audit["document_bytes"].values())


def test_preflight_refuses_dirty_production_source(reviewed_repo):
    source = next(iter(c.SOURCE_BLOBS))
    (reviewed_repo / source).write_text("# unreviewed source\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="unexpected tracked changes"):
        c.preflight(reviewed_repo)


def test_preflight_refuses_unexpected_tracked_path(reviewed_repo):
    file = reviewed_repo / "extra.py"
    file.write_text("x = 1\n", encoding="utf-8")
    git(reviewed_repo, "add", "extra.py")
    with pytest.raises(RuntimeError, match="staged"):
        c.preflight(reviewed_repo)


def test_preflight_refuses_unreviewed_document_change(reviewed_repo):
    doc = reviewed_repo / "docs/roadmap.md"
    doc.write_bytes(doc.read_bytes() + b"\nunknown addition\n")
    with pytest.raises(RuntimeError, match="unexpected content"):
        c.preflight(reviewed_repo)


def test_preflight_accepts_committed_five_docs_in_descendant(reviewed_repo):
    git(reviewed_repo, "add", "README.md", "docs")
    git(reviewed_repo, "commit", "-qm", "commit reviewed R2 docs")
    git(reviewed_repo, "push", "-q", "origin", "develop")
    audit = c.preflight(reviewed_repo)
    assert audit["tracked_before"] == []
    assert set(audit["committed_delta"]) == set(c.BASE_DOC_BLOBS)


def test_preflight_refuses_unrelated_committed_code(reviewed_repo):
    source = next(iter(c.SOURCE_BLOBS))
    (reviewed_repo / source).write_text("# changed source\n", encoding="utf-8")
    git(reviewed_repo, "add", source)
    git(reviewed_repo, "commit", "-qm", "unreviewed code")
    git(reviewed_repo, "push", "-q", "origin", "develop")
    with pytest.raises(RuntimeError, match="unexpected committed files"):
        c.preflight(reviewed_repo)


def test_dry_run_runs_no_full_suite_and_changes_no_docs(reviewed_repo, tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    monkeypatch.setattr(c, "run_full_suite", lambda *args: pytest.fail("full suite invoked in dry-run"))
    before = {p: (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS}
    assert c.run(reviewed_repo, dry_run=True, resume_report=None) == 0
    assert before == {p: (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS}


def test_successful_end_gate_writes_five_full_docs(reviewed_repo, tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    calls = []
    def fake_full(root, output):
        calls.append(True)
        return 3555, "3555 passed in 39.12s", 0
    monkeypatch.setattr(c, "run_full_suite", fake_full)
    assert c.run(reviewed_repo, dry_run=False, resume_report=None) == 0
    assert len(calls) == 1
    assert all(c.FINAL_MARKER in (reviewed_repo / p).read_text(encoding="utf-8") for p in c.BASE_DOC_BLOBS)
    folders = list((tmp_path / "local" / "EHPProofTracerRecovery").glob("phase171_closeout_r3_*/"))
    assert len(folders) == 1
    folder = folders[0]
    with zipfile.ZipFile(folder / "PHASE171_FINAL_FIVE_FULL_DOCUMENTS.zip") as z:
        assert set(z.namelist()) == set(c.BASE_DOC_BLOBS)
        for path in c.BASE_DOC_BLOBS:
            assert z.read(path) == (reviewed_repo / path).read_bytes()


def test_failed_end_gate_never_changes_documents(reviewed_repo, tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    before = {p: (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS}
    def fake_fail(root, output):
        raise RuntimeError("pytest failed")
    monkeypatch.setattr(c, "run_full_suite", fake_fail)
    assert c.run(reviewed_repo, dry_run=False, resume_report=None) == 1
    assert before == {p: (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS}


def test_windows_runner_passes_named_arguments():
    runner = (Path(__file__).resolve().parents[1] / "run.ps1").read_text(encoding="utf-8")
    assert "& python @PythonArguments" in runner
    assert "& python @Args" not in runner
    assert "if ($DryRun)" in runner
    assert "'--resume-report'" in runner


def test_nonzero_full_suite_stores_exit_and_does_not_close(reviewed_repo, tmp_path, monkeypatch):
    import json
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    before = {p: (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS}
    monkeypatch.setattr(c, "run_full_suite", lambda root, output: (0, "FULL_SUITE_FAILED_EXIT_1", 1))
    assert c.run(reviewed_repo, dry_run=False, resume_report=None) == 1
    assert before == {p: (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS}
    reports = list((tmp_path / "local" / "EHPProofTracerRecovery").glob("phase171_closeout_r3_*/closeout.json"))
    assert len(reports) == 1
    report = json.loads(reports[0].read_text(encoding="utf-8"))
    assert report["pytest_exit"] == 1
    assert report["full_suite_verified"] is False
    assert report["result"] == "REFUSED_OR_FAILED"


def test_resume_a_verified_gate_without_second_full_suite(reviewed_repo, tmp_path, monkeypatch):
    import json
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    baseline = c.preflight(reviewed_repo)
    report_file = tmp_path / "verified.json"
    report_file.write_text(json.dumps({
        "phase": "171_CLOSEOUT_R3", "pytest_exit": 0,
        "full_suite_verified": True, "pytest_passed": 3561,
        "pytest_summary": "3561 passed in 40.31s",
        "preflight": {"head": baseline["head"]},
        "documents_before_sha256": baseline["document_sha256"],
    }), encoding="utf-8")
    monkeypatch.setattr(c, "run_full_suite", lambda *args: pytest.fail("full suite attempted twice"))
    assert c.run(reviewed_repo, dry_run=False, resume_report=report_file) == 0
    assert all(c.FINAL_MARKER.encode("ascii") in (reviewed_repo / p).read_bytes() for p in c.BASE_DOC_BLOBS)
