"""R10ET-R6D: guarded R6 audit certification update and focused rerun."""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path

sys.dont_write_bytecode = True

from .patch import (
    EXPECTED_HEAD, R6C_PATCH, R6C_PATCH_SHA256, TARGET, sha256_hex,
    transform_r6_audit, whole_function,
)


def git(root: Path, *arguments: str, check: bool = True) -> bytes:
    result = subprocess.run(
        ("git", "-C", str(root), *arguments),
        capture_output=True, check=check,
    )
    return result.stdout


def snapshot(root: Path) -> dict[str, str]:
    return {
        "head": git(root, "rev-parse", "HEAD").decode("ascii").strip(),
        "staged_raw": git(root, "diff", "--cached", "--raw", "-z").hex(),
        "tracked_raw": git(root, "diff", "--raw", "-z").hex(),
    }


def guard(root: Path) -> bytes:
    if git(root, "branch", "--show-current").decode().strip() != "develop":
        raise RuntimeError("R6D requires develop branch")
    if git(root, "rev-parse", "HEAD").decode().strip() != EXPECTED_HEAD:
        raise RuntimeError("R6D refuses unknown Git HEAD")
    if sha256_hex((root / R6C_PATCH).read_bytes()) != R6C_PATCH_SHA256:
        raise RuntimeError("R6D refuses unknown R6C patch source")
    if not (root / "phase169_r10et_r6c_root_reachable_citations/audit.py").is_file():
        raise RuntimeError("R6D requires completed R6C package")
    if not (root / "phase169_r10et_r5d_staged_audit_guard/patch.py").is_file():
        raise RuntimeError("R6D requires previous R5D package")
    # A tracked audit file may have existing staged edits; do not overwrite it.
    result = subprocess.run(("git", "-C", str(root), "ls-files", "--error-unmatch", "--", TARGET),
                            capture_output=True)
    if result.returncode == 0:
        raise RuntimeError("R6D refuses a tracked R6 audit")
    original = (root / TARGET).read_bytes()
    transform_r6_audit(original)
    return original


def execute(root: Path) -> int:
    print("R10ET_R6D_MODE=R6_AUDIT_CERTIFICATION_UPDATE", flush=True)
    original = guard(root)
    updated = transform_r6_audit(original)
    before = snapshot(root)
    external = Path(os.environ.get("LOCALAPPDATA", os.environ.get("TEMP", "")))
    if not external.is_absolute():
        raise RuntimeError("R6D requires LOCALAPPDATA or TEMP outside repository")
    backup_base = external / "EHPProofTracerRecovery"
    if root == backup_base or root in backup_base.parents or backup_base in root.parents:
        raise RuntimeError("R6D refuses backup inside repository")
    suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup = backup_base / f"r10et_r6d_{suffix}"
    backup.mkdir(parents=True, exist_ok=False)
    (backup / "audit_before.py").write_bytes(original)
    (backup / "audit_after.py").write_bytes(updated)
    (backup / "certify_reviewed_production_FULL.py").write_text(whole_function(updated), encoding="utf-8")
    (backup / "state_before.json").write_text(json.dumps(before, indent=2) + "\n", encoding="utf-8")
    print(f"R10ET_R6D_BACKUP={backup}", flush=True)

    target = root / TARGET
    patched = False
    try:
        target.write_bytes(updated)
        patched = True
        print(f"R10ET_R6D_PATCHED={TARGET}", flush=True)
        # R6 reruns the real 19 cases, then focused pytest with cache disabled.
        proc = subprocess.run(("powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                               "-File", str(root / "phase169_r10et_r6_residual_definition_dependency_audit/run.ps1")),
                              cwd=root)
        print(f"R10ET_R6D_R6_EXIT={proc.returncode}", flush=True)
        if proc.returncode:
            raise RuntimeError("R6 rerun failed after R6C-aware source certification")
        if snapshot(root) != before:
            raise RuntimeError("R6D detected a changed tracked Git diff/index/HEAD")
        if target.read_bytes() != updated:
            raise RuntimeError("R6D target was altered during audit")
        print("R10ET_R6D_TRACKED_INDEX_PRESERVED=True", flush=True)
        print("R10ET_R6D_COMPLETE=PASS", flush=True)
        print("R10ET_R6D_EXIT=0", flush=True)
        return 0
    except BaseException:
        print("R10ET_R6D_ERROR=" + traceback.format_exc(), flush=True)
        if patched and target.read_bytes() == updated:
            target.write_bytes(original)
            print("R10ET_R6D_ROLLBACK=True", flush=True)
        elif patched:
            print("R10ET_R6D_ROLLBACK_SKIPPED_CONCURRENT_EDIT=True", flush=True)
        print("R10ET_R6D_EXIT=1", flush=True)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    try:
        return execute(args.repo.resolve())
    except BaseException:
        print("R10ET_R6D_ERROR=" + traceback.format_exc(), flush=True)
        print("R10ET_R6D_EXIT=1", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
