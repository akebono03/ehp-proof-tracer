"""Guarded one-file Phase 170 R3-R5 installer, focused tests, and rollback."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

BASE_HEAD = "5a49800274157fa6b8e58aa7c372cee7d17e0195"
REVIEWED_HEAD = "32377a9fa4dde75ee0366c7460287354a137536f"
BASE_BLOB = "4e53bccc9f40e65eb91f0c7fc608cc99a68898cb"
TARGET = "phase168_r2_toda52_transport.py"
ALLOWED_ADDED = (
    "phase170_r3_r4_n2_generalization_audit/DESIGN_JA.md",
    "phase170_r3_r4_n2_generalization_audit/README.md",
    "phase170_r3_r4_n2_generalization_audit/__init__.py",
    "phase170_r3_r4_n2_generalization_audit/audit.py",
    "phase170_r3_r4_n2_generalization_audit/run.ps1",
    "phase170_r3_r4_n2_generalization_audit/tests/test_audit_contract.py",
)


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=root, text=True,
                          encoding="utf-8", errors="replace", capture_output=True)
    if proc.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc.stdout.strip()


def preflight(root: Path) -> dict:
    branch = git(root, "branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("Phase 170 R3-R5 requires develop")
    head = git(root, "rev-parse", "HEAD")
    if head not in (BASE_HEAD, REVIEWED_HEAD):
        raise RuntimeError(f"unreviewed HEAD: {head}")
    if head == REVIEWED_HEAD:
        rows = git(root, "diff", "--name-status", BASE_HEAD, REVIEWED_HEAD).splitlines()
        expected = {"A\t" + item for item in ALLOWED_ADDED}
        if set(rows) != expected:
            raise RuntimeError("unreviewed change between approved HEADs")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked source/index changes exist; refusing patch")
    blob = git(root, "rev-parse", f"HEAD:{TARGET}")
    if blob != BASE_BLOB:
        raise RuntimeError("reviewed original module blob mismatch")
    module = root / TARGET
    if not module.is_file():
        raise RuntimeError("production module missing")
    source = module.read_bytes()
    replacement = Path(__file__).resolve().parent / "replacement" / TARGET
    data = replacement.read_bytes()
    compile(data, TARGET, "exec")
    if not (b"def _toda52_rule(" in source and b"def expand_toda52_finite_cyclic_goal(" in source):
        raise RuntimeError("reviewed production function shapes missing")
    if source == data:
        raise RuntimeError("patch already applied; not overwriting")
    return {
        "branch": branch,
        "head": head,
        "old_sha256": hashlib.sha256(source).hexdigest(),
        "new_sha256": hashlib.sha256(data).hexdigest(),
    }


def run_process(root: Path, output: Path, name: str, args: list[str]) -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(args, cwd=root, text=True, encoding="utf-8",
                          errors="replace", stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, env=env)
    (output / f"{name}.log").write_text(proc.stdout, encoding="utf-8")
    print(proc.stdout, flush=True)
    print(f"PHASE170_R3R5_{name.upper()}_EXIT={proc.returncode}", flush=True)
    return proc.returncode


def run(root: Path, *, dry_run: bool) -> int:
    package = Path(__file__).resolve().parent
    output_base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery"
    output = output_base / ("phase170_r3_r5_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    report = {"phase": "170 R3-R5", "mode": "DRY_RUN" if dry_run else "ONE_FILE_GUARDED_PATCH", "output": str(output)}
    print(f"PHASE170_R3R5_OUTPUT={output}", flush=True)
    try:
        review = preflight(root)
        report.update(review)
        original = (root / TARGET).read_bytes()
        replacement = (package / "replacement" / TARGET).read_bytes()
        backup = output / "phase168_r2_toda52_transport.py.before"
        backup.write_bytes(original)
        if dry_run:
            print("PHASE170_R3R5_DRY_RUN=PASS", flush=True)
            report["result"] = "DRY_RUN_PASS"
            return 0
        changed = False
        try:
            (root / TARGET).write_bytes(replacement)
            changed = True
            test_files = [
                str(package / "tests" / "test_phase170_r3_r5_toda52_cyclic.py"),
                str(root / "phase168_r2_toda52_transport" / "tests" / "test_phase168_r2_toda52_transport.py"),
                str(root / "tests" / "test_phase167_r3_generic_resolver.py"),
            ]
            code = run_process(root, output, "focused_pytest", [
                sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
                "-p", "no:cacheprovider", *test_files,
            ])
            if code:
                raise RuntimeError(f"focused pytest failed: {code}")
            code = run_process(root, output, "active_web", [
                sys.executable, "-B", str(package / "verify.py"),
            ])
            if code:
                raise RuntimeError(f"pi_5^2 proof or public Web verification failed: {code}")
            changed = False
            report["result"] = "PATCHED_AND_VERIFIED"
            report["tracked_changed"] = [TARGET]
            print("PHASE170_R3R5_RESULT=PATCHED_AND_VERIFIED", flush=True)
            print("PHASE170_R3R5_FULL_PYTEST=False", flush=True)
            return 0
        finally:
            if changed:
                (root / TARGET).write_bytes(original)
                print("PHASE170_R3R5_ROLLBACK=RESTORED_ORIGINAL", flush=True)
    except Exception as exc:
        report["result"] = "REFUSED_OR_ROLLED_BACK"
        report["error"] = repr(exc)
        print(f"PHASE170_R3R5_REFUSED={type(exc).__name__}: {exc}", flush=True)
        return 2
    finally:
        (output / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"PHASE170_R3R5_REPORT={output / 'result.json'}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
