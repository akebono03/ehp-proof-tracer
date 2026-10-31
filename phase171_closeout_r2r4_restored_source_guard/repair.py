"""Phase 171 R2R4: repair R2R3 content guard for restored original R2 files.

The only persistent code edit is R2R3/install.py. The reviewed R2R3
installer subsequently owns the five document outputs and their rollback.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
R2 = ROOT / "phase171_closeout_r2_documentation_full_output"
R2R3 = ROOT / "phase171_closeout_r2r3_mixed_line_ending_fix"
TARGET = R2R3 / "install.py"
REVIEWED_HEAD = "3e74849bf90bc115c16503ddd46d49996baa0856"
REVIEWED_OLD_INSTALL = "71016ec5e80c55b353d131922d27ffcb3ef68bc48572ed090060512670f74a0b"
REVIEWED_NEW_INSTALL = "12b26ec3a0591a6498e9f9953b640c31d9a5104f829dc136a9cba091ef4fdbbd"
REVIEWED_PAIRS = {
    "R2_BASE": {
        "update_docs.py": "19a65bc5b3e4c2ea38ec8216cc320bade803e5daa247e58f3075a4e79a59f247",
        "tests/test_document_writer.py": "ce7a2065ea346c879e29fe1258f919c375aba5bfe2877721b2e3af75759fb062",
    },
    "R2R1": {
        "update_docs.py": "b8e11ea6f762ca7fc6699cc45a7878f448ab966fc1eee316ad1e63f7f8e65dae",
        "tests/test_document_writer.py": "5ce255360fcdafd1498bbec6f4fefb8fa862e2c5f792b686f266aa98aadadf65",
    },
    "R2R3": {
        "update_docs.py": "8b39e61e57d171b2bf451137fd28730fca283364f726740a0cb543b808fd05d1",
        "tests/test_document_writer.py": "d0da01d85904e496ac9297275b2108cbd00be1fb0bdf887ae5badb00114a0b1e",
    },
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def write_atomic(path: Path, contents: bytes) -> None:
    fd, temp = tempfile.mkstemp(prefix=".phase171_r2r4_", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(contents)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def detect_reviewed_pair() -> str:
    actual = {name: sha((R2 / name).read_bytes()) for name in REVIEWED_PAIRS["R2_BASE"]}
    for state, expected in REVIEWED_PAIRS.items():
        if actual == expected:
            return state
    raise RuntimeError("unreviewed or mixed R2 writer/test source bytes: " + str(actual))


def preflight() -> tuple[bytes, bytes, bool, str]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD")
    if head != REVIEWED_HEAD or git("rev-parse", "origin/develop") != head:
        raise RuntimeError("unreviewed HEAD or origin/develop")
    if git("diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged changes refused")
    if git("diff", "--name-only", "HEAD", "--"):
        raise RuntimeError("unexpected tracked changes before R2 closeout")
    original = TARGET.read_bytes()
    correction = (HERE / "replacements" / "install.py").read_bytes()
    state = detect_reviewed_pair()
    if sha(correction) != REVIEWED_NEW_INSTALL:
        raise RuntimeError("R2R4 replacement installer integrity failure")
    if sha((HERE / "reviewed_originals" / "install.py").read_bytes()) != REVIEWED_OLD_INSTALL:
        raise RuntimeError("R2R4 inspected installer source integrity failure")
    before_hash = sha(original)
    if before_hash not in {REVIEWED_OLD_INSTALL, REVIEWED_NEW_INSTALL}:
        raise RuntimeError("unreviewed R2R3 installer content")
    for name, expected in REVIEWED_PAIRS["R2_BASE"].items():
        if sha((HERE / "reviewed_originals" / name).read_bytes()) != expected:
            raise RuntimeError("R2R4 inspected original R2 source changed: " + name)
    if not (R2R3 / "run.ps1").is_file():
        raise RuntimeError("R2R3 runner missing")
    print("PHASE171_CLOSEOUT_R2R4_HEAD=" + head, flush=True)
    print("PHASE171_CLOSEOUT_R2R4_R2_SOURCE_STATE=" + state, flush=True)
    print("PHASE171_CLOSEOUT_R2R4_ALREADY_CORRECTED=" + str(before_hash == REVIEWED_NEW_INSTALL), flush=True)
    print("PHASE171_CLOSEOUT_R2R4_CONTENT_GUARD=PASS", flush=True)
    return original, correction, before_hash == REVIEWED_NEW_INSTALL, state


def run(command: list[str]) -> int:
    result = subprocess.run(command, cwd=ROOT,
                            env={**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"},
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace")
    print(result.stdout, end="" if result.stdout.endswith("\n") else "\n", flush=True)
    return result.returncode


def output_dir() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery"
    directory = base / ("phase171_closeout_r2r4_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    directory.mkdir(parents=True, exist_ok=False)
    return directory


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    original, correction, already, state = preflight()
    if args.dry_run:
        print("PHASE171_CLOSEOUT_R2R4_RESULT=PASS_DRY_RUN", flush=True)
        return 0
    output = output_dir()
    (output / "BEFORE_R2R3_installer.py").write_bytes(original)
    report = {"phase": "171_CLOSEOUT_R2R4", "head": REVIEWED_HEAD,
              "source_state": state, "already_corrected": already, "full_pytest": False}
    success = False
    try:
        if original != correction:
            write_atomic(TARGET, correction)
        # This extra test covers the original R2 pair that caused the regression.
        code = run([sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
                    "--disable-warnings", "-p", "no:cacheprovider",
                    str(HERE / "tests" / "test_repair.py")])
        report["guard_pytest_exit"] = code
        if code:
            raise RuntimeError("R2R4 guard pytest failed")
        code = run([sys.executable, "-B", str(TARGET), "--dry-run"])
        report["r2r3_dry_run_exit"] = code
        if code:
            raise RuntimeError("R2R3 preflight after guard repair failed")
        code = run([sys.executable, "-B", str(TARGET)])
        report["r2r3_exit"] = code
        if code:
            raise RuntimeError("R2R3 full-document update failed")
        if TARGET.read_bytes() != correction:
            raise RuntimeError("R2R3 installer modified unexpectedly")
        expected_docs = {"README.md", "docs/design.md", "docs/development_log.md",
                         "docs/roadmap.md", "docs/proof_records.md"}
        tracked = set(filter(None, git("diff", "--name-only", "HEAD", "--").splitlines()))
        if tracked != expected_docs:
            raise RuntimeError("expected exactly five changed documents; found " + str(sorted(tracked)))
        success = True
        report["result"] = "PASS_FIVE_DOCUMENTS_PENDING_PHASE_END"
        print("PHASE171_CLOSEOUT_R2R4_RESULT=PASS_FIVE_DOCUMENTS_PENDING_PHASE_END", flush=True)
        return 0
    except Exception as exc:
        report["result"] = "FAIL_RESTORED_R2R4_INSTALLER"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        print("PHASE171_CLOSEOUT_R2R4_ERROR=" + str(exc), flush=True)
        return 1
    finally:
        if not success and TARGET.read_bytes() != original:
            write_atomic(TARGET, original)
        report["tracked_after"] = git("diff", "--name-only", "HEAD", "--").splitlines()
        (output / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE171_CLOSEOUT_R2R4_REPORT=" + str(output / "audit.json"), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
