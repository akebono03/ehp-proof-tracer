"""Phase 169 R4: audit and optionally commit exactly five finalized documents.

No full-suite pytest, production edits, cleaning, restoring, reset or push.
Audit-only is the default. --commit is an explicit opt-in operation.
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

REVIEWED_HEAD = "1e881f45b2f3f3ecbb1052750c9d7a7b5bf95712"
R1_HEAD = "15495f146ed07dbd04e374763c24d61262b6ac65"
R1_DIR = "phase169_closeout_r1_20261028_193510_755227"
R3_DIR = "phase169_closeout_r3_20261028_195816_728887"
DOC_BLOBS = {
    "README.md": "c2c2c9236fdee03686518d05fa0ca7367b044a3b",
    "docs/design.md": "39f859dfe8a0ee208509efcb4dae7dc126812993",
    "docs/development_log.md": "9a68123a59d6acb2845ffc376aabc164a0102b45",
    "docs/roadmap.md": "0f5314a479a3549e99844ff8e0a94a4cf117023c",
    "docs/proof_records.md": "a993629e7ad2d4883f2c0d3e272eef47dcf29b9a",
}
DOCS = tuple(DOC_BLOBS)
DOC_MARKER = "<!-- PHASE169_FINAL_CLOSEOUT_20261028 -->"
MESSAGE = "docs: close Phase 169 after final regression gate"


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    process = subprocess.run(
        ["git", "-c", "core.longpaths=true", "-C", str(root), *args],
        capture_output=True, check=False, timeout=90, env=env,
    )
    if check and process.returncode:
        raise RuntimeError(
            "git " + " ".join(args) + " failed: "
            + process.stderr.decode("utf-8", "replace").strip()
        )
    return process


def git_text(root: Path, *args: str) -> str:
    return git(root, *args).stdout.decode("utf-8", "replace").strip()


def changed_names(root: Path, cached: bool) -> set[str]:
    args = ("diff", "--cached", "--name-only", "-z") if cached else (
        "diff", "--name-only", "-z"
    )
    raw = git(root, *args).stdout
    return {part.decode("utf-8", "surrogateescape") for part in raw.split(b"\0") if part}


def validate_report(report: dict[str, Any]) -> None:
    if not isinstance(report, dict):
        raise RuntimeError("Invalid R1 report type")
    expected = {
        "mode": "PHASE169_END_OF_PHASE_TEST",
        "head": R1_HEAD,
        "reviewed_files": 13,
        "r6_cases": 19,
        "git_index_preserved": True,
        "phase169_certified": False,
        "phase169_test_gate_pass": True,
        "decision": "TEST_GATE_PASS_PENDING_PHASE169_CLOSEOUT_DOCUMENTATION",
    }
    for key, value in expected.items():
        if report.get(key) != value or type(report.get(key)) is not type(value):
            raise RuntimeError("R1 report mismatch: " + key)
    for key, count in (("focused", 67), ("active_full", 3546)):
        entry = report.get(key)
        if not isinstance(entry, dict):
            raise RuntimeError("Missing R1 pytest evidence: " + key)
        if (entry.get("exit_code") != 0 or type(entry.get("exit_code")) is not int
                or entry.get("passed_count") != count
                or type(entry.get("passed_count")) is not int):
            raise RuntimeError("R1 pytest result mismatch: " + key)
        command = entry.get("command")
        if not isinstance(command, list) or "pytest" not in command or "-p" not in command:
            raise RuntimeError("R1 pytest command missing: " + key)
        if "no:cacheprovider" not in command:
            raise RuntimeError("R1 cache-disabled condition missing: " + key)
        if key == "active_full" and command[-1] != "tests":
            raise RuntimeError("R1 active test scope changed")
        log_path = Path(entry.get("log", ""))
        if not log_path.is_file():
            raise RuntimeError("R1 pytest log not found: " + key)
        log_text = log_path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"\b" + str(count) + r" passed\b", log_text) is None:
            raise RuntimeError("R1 pytest log count inconsistent: " + key)
        if re.search(r"\b(?:\d+ failed|\d+ error)\b", log_text):
            raise RuntimeError("R1 pytest log contains a failure: " + key)


def locate_full_copy(folder: Path, relative: str) -> Path:
    direct = folder / relative
    if direct.is_file():
        return direct
    matches = list(folder.rglob(Path(relative).name)) if folder.is_dir() else []
    if len(matches) == 1 and matches[0].is_file():
        return matches[0]
    raise RuntimeError("Expected unique full document copy for " + relative + " under " + str(folder))


def validate_manifest(manifest: dict[str, Any], root: Path, recovery: Path) -> None:
    if not isinstance(manifest, dict):
        raise RuntimeError("Invalid documentation manifest")
    expected = {
        "mode": "PHASE169_FINAL_DOCUMENTATION",
        "repository": "akebono03/ehp-proof-tracer",
        "local_head_before": REVIEWED_HEAD,
        "origin_develop_before": REVIEWED_HEAD,
        "reviewed_remote_head": REVIEWED_HEAD,
        "test_report_head": R1_HEAD,
        "focused_pass": 67,
        "active_full_pass": 3546,
        "applied": True,
        "index_preserved": True,
        "remote_ahead_of_local": False,
    }
    for key, value in expected.items():
        if manifest.get(key) != value or type(manifest.get(key)) is not type(value):
            raise RuntimeError("R3 manifest mismatch: " + key)
    expected_report = recovery / R1_DIR / "report.json"
    if Path(manifest.get("test_report", "")) != expected_report:
        raise RuntimeError("R3 does not reference the reviewed R1 report")
    files = manifest.get("files")
    if not isinstance(files, dict) or set(files) != set(DOCS):
        raise RuntimeError("R3 manifest lists unexpected documents")
    base = recovery / R3_DIR
    for relative in DOCS:
        entry = files[relative]
        if not isinstance(entry, dict) or entry.get("old_blob") != DOC_BLOBS[relative]:
            raise RuntimeError("R3 original Git blob mismatch: " + relative)
        source = root / relative
        if not source.is_file():
            raise RuntimeError("Closeout document missing: " + relative)
        current = source.read_bytes()
        if hashlib.sha256(current).hexdigest() != entry.get("new_sha256"):
            raise RuntimeError("R3 final document checksum changed: " + relative)
        if locate_full_copy(base / "after_full", relative).read_bytes() != current:
            raise RuntimeError("R3 after_full differs from current file: " + relative)
        backup = locate_full_copy(base / "before_full", relative)
        recorded_blob = git_text(root, "hash-object", "--path=" + relative, str(backup))
        if recorded_blob != DOC_BLOBS[relative]:
            raise RuntimeError("R3 before_full does not match reviewed original: " + relative)
        content = current.decode("utf-8")
        if content.count(DOC_MARKER) != 1 or "Phase 169" not in content:
            raise RuntimeError("Final closeout marker invalid: " + relative)
        if current == backup.read_bytes():
            raise RuntimeError("No documented change in " + relative)


def inspect(root: Path, recovery: Path) -> None:
    if git_text(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Git branch is not develop")
    head = git_text(root, "rev-parse", "HEAD")
    if head != REVIEWED_HEAD:
        raise RuntimeError("Unexpected local HEAD; refuse commit: " + head)
    origin = git_text(root, "rev-parse", "refs/remotes/origin/develop")
    if origin != head:
        raise RuntimeError("origin/develop differs from local HEAD")
    remote_line = git_text(root, "ls-remote", "origin", "refs/heads/develop")
    if remote_line != head + "\trefs/heads/develop":
        raise RuntimeError("Remote develop has changed; do not pull automatically")
    if changed_names(root, cached):
        raise RuntimeError("Pre-existing staged changes; will not touch index")
    working = changed_names(root, False)
    if working != set(DOCS):
        raise RuntimeError("Tracked changes differ from exactly the five closeout docs: " + str(working))
    for relative, blob in DOC_BLOBS.items():
        if git_text(root, "rev-parse", "HEAD:" + relative) != blob:
            raise RuntimeError("Unreviewed committed baseline: " + relative)
    git(root, "diff", "--check", "--", *DOCS)
    report_path = recovery / R1_DIR / "report.json"
    manifest_path = recovery / R3_DIR / "manifest.json"
    if not report_path.is_file() or not manifest_path.is_file():
        raise RuntimeError("R1 report or R3 manifest missing from LOCALAPPDATA")
    validate_report(json.loads(report_path.read_text(encoding="utf-8")))
    validate_manifest(json.loads(manifest_path.read_text(encoding="utf-8")), root, recovery)
    print("PHASE169_CLOSEOUT_R4_BASE_HEAD=" + head, flush=True)
    print("PHASE169_CLOSEOUT_R4_TEST_GATE=67_FOCUSED_3546_ACTIVE_PASS", flush=True)
    print("PHASE169_CLOSEOUT_R4_DOCUMENTS=5/5_VERIFIED", flush=True)
    print("PHASE169_CLOSEOUT_R4_TRACKED_SCOPE=ONLY_FIVE_DOCUMENTS", flush=True)
    print("PHASE169_CLOSEOUT_R4_REMOTE_MATCH=True", flush=True)


def execute(root: Path, commit: bool) -> int:
    localappdata = os.environ.get("LOCALAPPDATA")
    if not localappdata:
        raise RuntimeError("LOCALAPPDATA is required")
    recovery = Path(localappdata).resolve() / "EHPProofTracerRecovery"
    if root == recovery or root in recovery.parents or recovery in root.parents:
        raise RuntimeError("Recovery output must be outside Git checkout")
    inspect(root, recovery)
    if not commit:
        print("PHASE169_CLOSEOUT_R4_DECISION=READY_FOR_EXPLICIT_COMMIT", flush=True)
        print("PHASE169_CLOSEOUT_R4_EXIT=0", flush=True)
        return 0
    output = recovery / ("phase169_closeout_r4_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    (output / "precommit_diff.patch").write_bytes(git(root, "diff", "--binary", "--", *DOCS).stdout)
    (output / "precommit_stat.txt").write_text(
        git_text(root, "diff", "--stat", "--", *DOCS) + "\n", encoding="utf-8"
    )
    print("PHASE169_CLOSEOUT_R4_PRECOMMIT_BACKUP=" + str(output), flush=True)
    # A second guard immediately before index changes.
    inspect(root, recovery)
    git(root, "add", "--", *DOCS)
    staged = changed_names(root, True)
    if staged != set(DOCS):
        raise RuntimeError("Unexpected staged paths; no commit executed: " + str(staged))
    if changed_names(root, False):
        raise RuntimeError("Unexpected unstaged tracked changes; no commit executed")
    git(root, "diff", "--cached", "--check", "--", *DOCS)
    git(root, "commit", "-m", MESSAGE)
    newhead = git_text(root, "rev-parse", "HEAD")
    if git_text(root, "rev-parse", "HEAD^") != REVIEWED_HEAD:
        raise RuntimeError("Committed parent is unexpected; inspect Git immediately")
    committed = {x for x in git_text(root, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines() if x}
    if committed != set(DOCS):
        raise RuntimeError("Unexpected files in new commit: " + str(committed))
    if changed_names(root, True) or changed_names(root, False):
        raise RuntimeError("Unexpected remaining tracked diffs after commit")
    summary = {
        "mode": "PHASE169_R4_FIVE_DOC_COMMIT",
        "head_before": REVIEWED_HEAD,
        "head_after": newhead,
        "changed_documents": sorted(DOCS),
        "pushed": False,
        "full_pytest_rerun": False,
        "historical_audit_folders_untouched": True,
    }
    (output / "commit_record.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE169_CLOSEOUT_R4_COMMIT_HEAD=" + newhead, flush=True)
    print("PHASE169_CLOSEOUT_R4_COMMITTED_DOCS=5/5", flush=True)
    print("PHASE169_CLOSEOUT_R4_PUSH_NOT_RUN=True", flush=True)
    print("PHASE169_CLOSEOUT_R4_DECISION=PHASE169_DOCS_COMMITTED_LOCALLY_PENDING_PUSH", flush=True)
    print("PHASE169_CLOSEOUT_R4_EXIT=0", flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    try:
        return execute(args.repo.resolve(), args.commit)
    except BaseException:
        print("PHASE169_CLOSEOUT_R4_ERROR=" + traceback.format_exc(), flush=True)
        print("PHASE169_CLOSEOUT_R4_EXIT=1", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
