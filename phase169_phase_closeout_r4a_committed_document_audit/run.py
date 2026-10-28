"""Phase 169 R4A: verify already committed closeout without any Git writes.

The Phase 169 final documentation is already committed at 83b1400.
This program does not add, commit, push, pull, reset, restore, or clean files.
It does not rerun the full pytest suite.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import traceback
from typing import Any

sys.dont_write_bytecode = True

REPOSITORY = "akebono03/ehp-proof-tracer"
FINAL_HEAD = "83b1400d55890cea7b8ab44579c11e11f8dd8e69"
PARENT_HEAD = "1e881f45b2f3f3ecbb1052750c9d7a7b5bf95712"
TEST_HEAD = "15495f146ed07dbd04e374763c24d61262b6ac65"
R1_DIR = "phase169_closeout_r1_20261028_193510_755227"
R3_DIR = "phase169_closeout_r3_20261028_195816_728887"
MARKER = "<!-- PHASE169_FINAL_CLOSEOUT_20261028 -->"
DOCUMENT_BLOBS = {
    "README.md": "89b637a35134583fa58132d6ffc31519bee5bfff",
    "docs/design.md": "fb729605aa7ea67ef3586524af3f964965139ba8",
    "docs/development_log.md": "8dfbedc8d64b342833f390810399a3ebf988c554",
    "docs/roadmap.md": "ae9cbe4feb34c013312fe311fbcaf0ddf2534b81",
    "docs/proof_records.md": "74daf33c383c57f1727a171b83ae51ca92528cb0",
}
PREVIOUS_DOCUMENT_BLOBS = {
    "README.md": "c2c2c9236fdee03686518d05fa0ca7367b044a3b",
    "docs/design.md": "39f859dfe8a0ee208509efcb4dae7dc126812993",
    "docs/development_log.md": "9a68123a59d6acb2845ffc376aabc164a0102b45",
    "docs/roadmap.md": "0f5314a479a3549e99844ff8e0a94a4cf117023c",
    "docs/proof_records.md": "a993629e7ad2d4883f2c0d3e272eef47dcf29b9a",
}
AUDIT_PACKAGE_PATHS = frozenset((
    "phase169_phase_closeout_r3_documentation/DESIGN_JA.md",
    "phase169_phase_closeout_r3_documentation/README.md",
    "phase169_phase_closeout_r3_documentation/__init__.py",
    "phase169_phase_closeout_r3_documentation/run.ps1",
    "phase169_phase_closeout_r3_documentation/run.py",
    "phase169_phase_closeout_r3_documentation/tests/test_closeout.py",
    "phase169_phase_closeout_r3b_gate_head_fix/DESIGN_JA.md",
    "phase169_phase_closeout_r3b_gate_head_fix/README.md",
    "phase169_phase_closeout_r3b_gate_head_fix/__init__.py",
    "phase169_phase_closeout_r3b_gate_head_fix/reviewed_sources/inspect_report_AFTER_FULL.py",
    "phase169_phase_closeout_r3b_gate_head_fix/reviewed_sources/run_AFTER_FULL.py",
    "phase169_phase_closeout_r3b_gate_head_fix/reviewed_sources/run_BEFORE_FULL.py",
    "phase169_phase_closeout_r3b_gate_head_fix/run.ps1",
    "phase169_phase_closeout_r3b_gate_head_fix/run.py",
    "phase169_phase_closeout_r3b_gate_head_fix/tests/test_closeout.py",
    "phase169_phase_closeout_r3b_gate_head_fix/tests/test_gate_head.py",
))
EXPECTED_COMMIT_PATHS = frozenset(DOCUMENT_BLOBS) | AUDIT_PACKAGE_PATHS


def git(root: Path, *arguments: str) -> str:
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    process = subprocess.run(
        ["git", "-c", "core.longpaths=true", "-C", str(root), *arguments],
        capture_output=True, check=False, timeout=90, env=env,
    )
    if process.returncode:
        raise RuntimeError(
            "Git read failed: " + " ".join(arguments) + " :: "
            + process.stderr.decode("utf-8", "replace").strip()
        )
    return process.stdout.decode("utf-8", "replace").strip()


def git_bytes(root: Path, *arguments: str) -> bytes:
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    process = subprocess.run(
        ["git", "-c", "core.longpaths=true", "-C", str(root), *arguments],
        capture_output=True, check=False, timeout=90, env=env,
    )
    if process.returncode:
        raise RuntimeError("Git binary read failed: " + " ".join(arguments))
    return process.stdout


def verify_commit_scope(names: set[str]) -> None:
    if names != EXPECTED_COMMIT_PATHS:
        missing = sorted(EXPECTED_COMMIT_PATHS - names)
        unexpected = sorted(names - EXPECTED_COMMIT_PATHS)
        raise RuntimeError(
            "The already-published commit path inventory differs: "
            + "missing=" + repr(missing) + " unexpected=" + repr(unexpected)
        )


def verify_test_report(data: dict[str, Any], recovery: Path) -> dict[str, int]:
    expected = {
        "mode": "PHASE169_END_OF_PHASE_TEST",
        "head": TEST_HEAD,
        "reviewed_files": 13,
        "r6_cases": 19,
        "git_index_preserved": True,
        "phase169_certified": False,
        "phase169_test_gate_pass": True,
        "decision": "TEST_GATE_PASS_PENDING_PHASE169_CLOSEOUT_DOCUMENTATION",
    }
    if not isinstance(data, dict):
        raise RuntimeError("R1 report must be an object")
    for name, value in expected.items():
        if type(data.get(name)) is not type(value) or data.get(name) != value:
            raise RuntimeError("R1 report contract mismatch: " + name)
    counts: dict[str, int] = {}
    for name, expected_count in (("focused", 67), ("active_full", 3546)):
        entry = data.get(name)
        if not isinstance(entry, dict):
            raise RuntimeError("R1 report has no " + name + " result")
        if (type(entry.get("passed_count")) is not int
                or entry["passed_count"] != expected_count
                or type(entry.get("exit_code")) is not int
                or entry["exit_code"] != 0):
            raise RuntimeError("R1 result count or exit code incorrect: " + name)
        cmd = entry.get("command")
        if not isinstance(cmd, list) or not all(isinstance(x, str) for x in cmd):
            raise RuntimeError("R1 command missing: " + name)
        if "pytest" not in cmd or "-p" not in cmd or "no:cacheprovider" not in cmd:
            raise RuntimeError("R1 command changed: " + name)
        if name == "active_full" and (not cmd or cmd[-1] != "tests"):
            raise RuntimeError("R1 active tests scope changed")
        log = Path(entry.get("log", ""))
        if log.parent.resolve() != (recovery / R1_DIR).resolve() or not log.is_file():
            raise RuntimeError("R1 evidence log missing or outside reviewed folder: " + name)
        contents = log.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"\b" + str(expected_count) + r" passed\b", contents):
            raise RuntimeError("R1 pass count does not match log: " + name)
        if re.search(r"\b\d+ (?:failed|error|errors)\b", contents):
            raise RuntimeError("R1 log reports failures: " + name)
        counts[name] = expected_count
    return counts


def verify_manifest(data: dict[str, Any], root: Path, recovery: Path) -> None:
    expected = {
        "mode": "PHASE169_FINAL_DOCUMENTATION",
        "repository": REPOSITORY,
        "local_head_before": PARENT_HEAD,
        "origin_develop_before": PARENT_HEAD,
        "reviewed_remote_head": PARENT_HEAD,
        "test_report_head": TEST_HEAD,
        "focused_pass": 67,
        "active_full_pass": 3546,
        "applied": True,
        "index_preserved": True,
        "remote_ahead_of_local": False,
    }
    if not isinstance(data, dict):
        raise RuntimeError("R3 manifest must be an object")
    for name, value in expected.items():
        if type(data.get(name)) is not type(value) or data.get(name) != value:
            raise RuntimeError("R3 manifest mismatch: " + name)
    expected_report = (recovery / R1_DIR / "report.json").resolve()
    if Path(data.get("test_report", "")).resolve() != expected_report:
        raise RuntimeError("R3 references an unexpected R1 test report")
    files = data.get("files")
    if not isinstance(files, dict) or set(files) != set(DOCUMENT_BLOBS):
        raise RuntimeError("R3 manifest has wrong document list")
    for relative, current_blob in DOCUMENT_BLOBS.items():
        entry = files[relative]
        if not isinstance(entry, dict) or entry.get("old_blob") != PREVIOUS_DOCUMENT_BLOBS[relative]:
            raise RuntimeError("R3 source blob mismatch: " + relative)
        raw = (root / relative).read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry.get("new_sha256"):
            raise RuntimeError("R3 final document checksum mismatch: " + relative)
        after = recovery / R3_DIR / "after_full" / relative
        before = recovery / R3_DIR / "before_full" / relative
        if not after.is_file() or after.read_bytes() != raw:
            raise RuntimeError("R3 after_full missing or inconsistent: " + relative)
        if not before.is_file() or before.read_bytes() == raw:
            raise RuntimeError("R3 before_full missing or unchanged: " + relative)
        if (git(root, "hash-object", "--path=" + relative, str(before))
                != PREVIOUS_DOCUMENT_BLOBS[relative]):
            raise RuntimeError("R3 original backup not identical to committed parent: " + relative)
        if git(root, "rev-parse", "HEAD^:" + relative) != PREVIOUS_DOCUMENT_BLOBS[relative]:
            raise RuntimeError("Commit parent document differs from reviewed one: " + relative)
        if git(root, "rev-parse", "HEAD:" + relative) != current_blob:
            raise RuntimeError("Published final document Git blob differs: " + relative)
        if git(root, "hash-object", "--path=" + relative, relative) != current_blob:
            raise RuntimeError("Working final document differs from commit: " + relative)
        content = raw.decode("utf-8")
        if content.count(MARKER) != 1:
            raise RuntimeError("Final closeout marker missing or duplicated: " + relative)


def index_digest(root: Path) -> str:
    index_location = Path(git(root, "rev-parse", "--git-path", "index"))
    if not index_location.is_absolute():
        index_location = root / index_location
    return hashlib.sha256(index_location.read_bytes()).hexdigest()


def execute(root: Path) -> int:
    recovery_env = os.environ.get("LOCALAPPDATA")
    if not recovery_env:
        raise RuntimeError("LOCALAPPDATA is required")
    recovery = (Path(recovery_env).resolve() / "EHPProofTracerRecovery").resolve()
    if recovery == root or root in recovery.parents or recovery in root.parents:
        raise RuntimeError("Recovery folder must be outside Git checkout")
    start_index = index_digest(root)
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    if head != FINAL_HEAD:
        raise RuntimeError("Expected already committed HEAD " + FINAL_HEAD + ", got " + head)
    if git(root, "rev-parse", "HEAD^") != PARENT_HEAD:
        raise RuntimeError("Unexpected document commit parent")
    if git(root, "rev-parse", "refs/remotes/origin/develop") != head:
        raise RuntimeError("Local origin/develop does not match committed HEAD")
    remote = git(root, "ls-remote", "origin", "refs/heads/develop")
    if remote != head + "\trefs/heads/develop":
        raise RuntimeError("GitHub develop differs from local commit; no Git changes made")
    unstaged = git_bytes(root, "diff", "--name-only", "-z")
    staged = git_bytes(root, "diff", "--cached", "--name-only", "-z")
    if unstaged or staged:
        raise RuntimeError("Tracked changes found; audit only, no modification")
    paths = git(root, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD")
    verify_commit_scope(set(paths.splitlines()))
    report_file = recovery / R1_DIR / "report.json"
    manifest_file = recovery / R3_DIR / "manifest.json"
    if not report_file.is_file() or not manifest_file.is_file():
        raise RuntimeError("Reviewed R1/R3 evidence is missing from LOCALAPPDATA")
    result = verify_test_report(json.loads(report_file.read_text(encoding="utf-8")), recovery)
    verify_manifest(json.loads(manifest_file.read_text(encoding="utf-8")), root, recovery)
    if index_digest(root) != start_index:
        raise RuntimeError("Git index changed during read-only audit")
    record = {
        "mode": "PHASE169_R4A_ALREADY_COMMITTED_READ_ONLY",
        "repository": REPOSITORY,
        "head": head,
        "parent": PARENT_HEAD,
        "committed_document_count": len(DOCUMENT_BLOBS),
        "additional_committed_audit_files": len(AUDIT_PACKAGE_PATHS),
        "focused_pass": result["focused"],
        "active_tests_pass": result["active_full"],
        "git_index_preserved": True,
        "tracked_clean": True,
        "new_commit_created": False,
        "push_run": False,
        "full_pytest_rerun": False,
        "decision": "PHASE169_CLOSED_COMMITTED_AND_SYNCED",
    }
    output = recovery / ("phase169_closeout_r4a_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    destination = output / "report.json"
    destination.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE169_CLOSEOUT_R4A_HEAD=" + head, flush=True)
    print("PHASE169_CLOSEOUT_R4A_DOCUMENTS=5/5_ALREADY_COMMITTED", flush=True)
    print("PHASE169_CLOSEOUT_R4A_COMMIT_SCOPE=5_DOCS_AND_16_AUDIT_FILES", flush=True)
    print("PHASE169_CLOSEOUT_R4A_TEST_GATE=67_FOCUSED_3546_ACTIVE_PASS", flush=True)
    print("PHASE169_CLOSEOUT_R4A_GIT_INDEX_PRESERVED=True", flush=True)
    print("PHASE169_CLOSEOUT_R4A_NEW_COMMIT=False", flush=True)
    print("PHASE169_CLOSEOUT_R4A_DECISION=PHASE169_CLOSED_COMMITTED_AND_SYNCED", flush=True)
    print("PHASE169_CLOSEOUT_R4A_REPORT=" + str(destination), flush=True)
    print("PHASE169_CLOSEOUT_R4A_EXIT=0", flush=True)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parsed = parser.parse_args(argv)
    try:
        return execute(parsed.repo.resolve())
    except BaseException:
        print("PHASE169_CLOSEOUT_R4A_ERROR=" + traceback.format_exc(), flush=True)
        print("PHASE169_CLOSEOUT_R4A_EXIT=1", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
