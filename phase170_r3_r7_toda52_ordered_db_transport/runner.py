"""Single-file guarded replacement with strict preflight and rollback."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

REVIEWED_HEAD = "84a9d8ad6110ed82b80bdeb7e9a0c5a361214de0"
REVIEWED_BLOB = "b3e104857e3a8129fb01df65ce3a38ff188ecd1f"
REVIEWED_SHA256 = "52a89e1ab91313c33d36253d1ce67075154503934ad5fe83d5fdf08916230afe"
TARGET = "phase168_r2_toda52_transport.py"


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ("git", *args), cwd=root, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {process.stderr.strip()}")
    return process.stdout.strip()


def preflight(root: Path) -> dict:
    branch, head = git(root, "branch", "--show-current"), git(root, "rev-parse", "HEAD")
    if branch != "develop" or head != REVIEWED_HEAD:
        raise RuntimeError(f"unreviewed branch/HEAD: {branch} {head}")
    if git(root, "diff", "--name-only") or git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("tracked worktree/index changes found; refusing to overwrite")
    if git(root, "rev-parse", f"HEAD:{TARGET}") != REVIEWED_BLOB:
        raise RuntimeError("reviewed source blob is different")
    target = root / TARGET
    if not target.is_file() or sha256(target.read_bytes()).hexdigest() != REVIEWED_SHA256:
        raise RuntimeError("on-disk source is not the reviewed Phase 170 R3-R5 implementation")
    for name in (
        "phase170_r3_r6_prop58_source.py",
        "phase169_r10e4_ordered_db_prior/db_prior.py",
        "phase168_r3_41p13_trust_boundary/verification.py",
    ):
        if not (root / name).is_file():
            raise RuntimeError(f"required reviewed dependency missing: {name}")
    return {"head": head, "branch": branch, "reviewed_blob": REVIEWED_BLOB}


def execute(root: Path, output: Path, name: str, command: list[str]) -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    process = subprocess.run(command, cwd=root, env=env, text=True,
                             encoding="utf-8", errors="replace",
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output / f"{name}.log").write_text(process.stdout, encoding="utf-8")
    print(process.stdout, flush=True)
    print(f"PHASE170_R3R7_{name.upper()}_EXIT={process.returncode}", flush=True)
    return process.returncode


def run(root: Path, dry_run: bool) -> int:
    package = Path(__file__).resolve().parent
    output = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery" / (
        "phase170_r3_r7_db_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    )
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE170_R3R7_MODE=GUARDED_TODA52_ORDERED_DB", flush=True)
    print(f"PHASE170_R3R7_OUTPUT={output}", flush=True)
    report = {"phase": "170 R3-R7 revised", "mode": "DRY_RUN" if dry_run else "ONE_FILE_GUARDED_PATCH"}
    target = root / TARGET
    changed = False
    passed = False
    original = None
    try:
        report.update(preflight(root))
        original = target.read_bytes()
        replacement = (package / "replacement" / TARGET).read_bytes()
        compile(replacement, TARGET, "exec")
        (output / "phase168_r2_toda52_transport.py.before").write_bytes(original)
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            print("PHASE170_R3R7_DRY_RUN=PASS", flush=True)
            passed = True
            return 0
        target.write_bytes(replacement)
        changed = True
        focused = [
            package / "tests" / "test_ordered_db_toda52.py",
            root / "phase168_r2_toda52_transport" / "tests" / "test_phase168_r2_toda52_transport.py",
            root / "phase170_r3_r5_toda52_cyclic_generalization" / "tests" / "test_phase170_r3_r5_toda52_cyclic.py",
            root / "phase169_r10e4_ordered_db_prior" / "tests" / "test_r10e4_ordered_db_prior.py",
            root / "phase170_r3_r6_prop58_pi73_source" / "tests" / "test_phase170_r3_r6_source.py",
        ]
        missing = [str(p) for p in focused if not p.is_file()]
        if missing:
            raise RuntimeError(f"focused test file missing: {missing!r}")
        status = execute(root, output, "focused_pytest", [
            sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
            "-p", "no:cacheprovider", *(str(path) for path in focused),
        ])
        if status:
            raise RuntimeError(f"focused pytest failed: {status}")
        status = execute(root, output, "active_web", [sys.executable, "-B", str(package / "verify.py")])
        if status:
            raise RuntimeError(f"active Web verification failed: {status}")
        report["result"] = "PATCHED_AND_WEB_VERIFIED"
        passed = True
        print("PHASE170_R3R7_RESULT=PATCHED_AND_WEB_VERIFIED", flush=True)
        print("PHASE170_R3R7_FULL_PYTEST=False", flush=True)
        return 0
    except Exception as error:
        report["result"] = "REFUSED_OR_ROLLED_BACK"
        report["error"] = repr(error)
        print(f"PHASE170_R3R7_REFUSED={type(error).__name__}: {error}", flush=True)
        return 2
    finally:
        if changed and not passed and original is not None:
            target.write_bytes(original)
            print("PHASE170_R3R7_ROLLBACK=RESTORED_R3R6_STATE", flush=True)
        report_path = output / "result.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"PHASE170_R3R7_REPORT={report_path}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
