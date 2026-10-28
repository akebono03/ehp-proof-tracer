"""Run the R3A safety check, R3-only patch and R3 audit with rollback."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime
import traceback

from phase169_r10et_closeout_r3a_committed_docs_head_fix.patch import (
    CURRENT_HEAD, TARGET, reviewed_patch,
)

def command(root: Path, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    result = subprocess.run(args, cwd=root, env=env, text=True,
                            encoding="utf-8", errors="replace", capture_output=True,
                            timeout=240, check=False)
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n", flush=True)
    if result.stderr:
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n", file=sys.stderr, flush=True)
    if check and result.returncode:
        raise RuntimeError(f"Command failed with exit={result.returncode}: {args}")
    return result

def git(root: Path, *args: str) -> str:
    proc = command(root, ["git", "-c", "core.longpaths=true", *args])
    return proc.stdout.strip()

def run(root: Path, package: Path) -> int:
    print("R10ET_CLOSEOUT_R3A_MODE=R3_AUDIT_ONLY_HEAD_FIX", flush=True)
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    if git(root, "rev-parse", "HEAD") != CURRENT_HEAD:
        raise RuntimeError("Local HEAD not the reviewed documentation commit")
    if git(root, "rev-parse", "refs/remotes/origin/develop") != CURRENT_HEAD:
        raise RuntimeError("Local tracking branch not the reviewed commit")
    if git(root, "ls-remote", "origin", "refs/heads/develop") != CURRENT_HEAD + "\trefs/heads/develop":
        raise RuntimeError("GitHub develop has moved: review before patch")
    if git(root, "diff", "--name-only") or git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Tracked files are not clean: preserving user changes")
    target = root / TARGET
    original = target.read_bytes()
    modified = reviewed_patch(root, package)
    root_abs = root.resolve()
    localappdata = os.environ.get("LOCALAPPDATA", "")
    if not localappdata:
        raise RuntimeError("LOCALAPPDATA must be defined")
    recovery = Path(localappdata).resolve() / "EHPProofTracerRecovery"
    if recovery == root_abs or recovery in root_abs.parents or root_abs in recovery.parents:
        raise RuntimeError("Backup path must be outside the repository")
    out = recovery / ("r10et_r3a_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    out.mkdir(parents=True, exist_ok=False)
    (out / "r3_audit_BEFORE_FULL.py").write_bytes(original)
    (out / "r3_audit_AFTER_FULL.py").write_bytes(modified)
    print("R10ET_CLOSEOUT_R3A_BACKUP=" + str(out), flush=True)
    changed = False
    try:
        if target.read_bytes() != original:
            raise RuntimeError("R3 audit source changed concurrently")
        target.write_bytes(modified)
        changed = True
        print("R10ET_CLOSEOUT_R3A_PATCHED=" + TARGET, flush=True)
        print("R10ET_CLOSEOUT_R3A_R3_RUN_START", flush=True)
        command(root, ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                       "-File", str(root / "phase169_r10et_closeout_r3_final_readonly_audit" / "run.ps1")])
        if target.read_bytes() != modified:
            raise RuntimeError("R3 audit source drifted during run")
        if git(root, "rev-parse", "HEAD") != CURRENT_HEAD:
            raise RuntimeError("Git HEAD changed during the audit")
        if git(root, "diff", "--name-only") or git(root, "diff", "--cached", "--name-only"):
            raise RuntimeError("Tracked Git files changed during the audit")
    except BaseException:
        if changed and target.read_bytes() == modified:
            target.write_bytes(original)
            print("R10ET_CLOSEOUT_R3A_ROLLBACK=RESTORED_ORIGINAL_R3_AUDIT", flush=True)
        raise
    print("R10ET_CLOSEOUT_R3A_INDEX_PRESERVED=True")
    print("R10ET_CLOSEOUT_R3A_FULL_PYTEST_NOT_RUN=True")
    print("R10ET_CLOSEOUT_R3A_COMPLETE=PASS")
    print("R10ET_CLOSEOUT_R3A_EXIT=0")
    return 0

def main() -> int:
    package = Path(__file__).resolve().parent
    root = package.parent
    try:
        return run(root, package)
    except BaseException:
        print("R10ET_CLOSEOUT_R3A_ERROR=" + traceback.format_exc(), flush=True)
        print("R10ET_CLOSEOUT_R3A_EXIT=1", flush=True)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
