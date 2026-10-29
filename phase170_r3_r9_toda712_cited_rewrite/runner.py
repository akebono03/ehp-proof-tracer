"""Guarded 3-file patch, focused tests, active Web check, rollback on failure."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha1, sha256
import json
import os
from pathlib import Path
import subprocess
import sys

REVIEWED_BASE_HEAD = "fdf60522b6d477209e9d8d67720a63f9863e419c"
REVIEWED_BLOBS = {
    "phase168_r2_toda52_transport.py": "3bf9dfa2080e330e7030f0f0a7762f3fb1fa8fff",
    "phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py": "84dfa0c6fe54e9d51b6b11279ee0001d6231ef8a",
    "sources/toda/Toda_06_2.tex": "76934583cff01c8ea83f768e26947eb9b556653b",
    "sources/toda/Toda_07_2.tex": "b5b366f2d2b72d7b419192fa74ab848eff098686",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
}
TARGETS = (
    "phase168_r2_toda52_transport.py",
    "phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py",
)
NEW_MODULE = "phase170_r3_r9_toda712_cited_rewrite"


def git(root: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", *args], cwd=root, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    if check and proc.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def preflight(root: Path) -> dict:
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != "develop" or head != REVIEWED_BASE_HEAD:
        raise RuntimeError(f"unreviewed branch or HEAD: {branch} {head}")
    if git(root, "diff", "--name-only") or git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("tracked worktree or staged changes present")
    for path, blob in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", f"HEAD:{path}") != blob or not (root/path).is_file():
            raise RuntimeError("reviewed file missing or changed: " + path)
    for target in TARGETS:
        raw = (root / target).read_bytes()
        normalized = raw.replace(b"\r\n", b"\n")
        def blobhash(data):
            return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()
        if blobhash(raw) != REVIEWED_BLOBS[target] and blobhash(normalized) != REVIEWED_BLOBS[target]:
            raise RuntimeError("worktree target differs from reviewed Git blob: " + target)
    return {"head": head, "branch": branch, "targets": list(TARGETS)}


def execute(root: Path, output: Path, name: str, command: list[str]) -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    run = subprocess.run(command, cwd=root, env=env, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                         errors="replace", check=False)
    (output / f"{name}.log").write_text(run.stdout, encoding="utf-8")
    print(run.stdout, flush=True)
    print(f"PHASE170_R3R9_{name.upper()}_EXIT={run.returncode}", flush=True)
    return run.returncode


def run(root: Path, *, dry_run: bool) -> int:
    package = Path(__file__).resolve().parent
    output = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery" / (
        "phase170_r3_r9_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    )
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE170_R3R9_MODE=CITED_GENERATOR_EQUALITY", flush=True)
    print(f"PHASE170_R3R9_OUTPUT={output}", flush=True)
    report = {"phase": "170 R3-R9", "mode": "DRY_RUN" if dry_run else "GUARDED_PATCH", "full_pytest": False}
    saved: dict[str, bytes] = {}
    modified: list[str] = []
    passed = False
    try:
        report["preflight"] = preflight(root)
        for target in TARGETS:
            original = (root / target).read_bytes()
            replacement = (package / "replacement" / target).read_bytes()
            compile(replacement, target, "exec")
            saved[target] = original
            (output / (Path(target).name + ".before")).write_bytes(original)
            if replacement == original or replacement.replace(b"\r\n",b"\n") == original.replace(b"\r\n",b"\n"):
                raise RuntimeError("replacement is unchanged: " + target)
        compile((package / "source712.py").read_bytes(), "source712.py", "exec")
        if dry_run:
            print("PHASE170_R3R9_DRY_RUN=PASS", flush=True)
            report["result"] = "DRY_RUN_PASS"
            passed = True
            return 0
        for target in TARGETS:
            dest = root / target
            dest.write_bytes((package / "replacement" / target).read_bytes())
            modified.append(target)
        focused = [
            package / "tests/test_toda712_rewrite.py",
            root / "phase170_r3_r7_toda52_ordered_db_transport/tests/test_ordered_db_toda52.py",
            root / "phase170_r3_r5_toda52_cyclic_generalization/tests/test_phase170_r3_r5_toda52_cyclic.py",
            root / "phase170_r3_r6_prop58_pi73_source/tests/test_phase170_r3_r6_source.py",
            root / "phase169_r10e4_ordered_db_prior/tests/test_r10e4_ordered_db_prior.py",
            root / "phase168_r2_toda52_transport/tests/test_phase168_r2_toda52_transport.py",
        ]
        if not all(path.is_file() for path in focused):
            raise RuntimeError("missing related focused test")
        ret = execute(root, output, "focused_pytest", [
            sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
            "-p", "no:cacheprovider", *(str(path) for path in focused),
        ])
        if ret:
            raise RuntimeError("focused pytest failed")
        ret = execute(root, output, "active_web", [
            sys.executable, "-B", str(package / "verify.py"),
        ])
        if ret:
            raise RuntimeError("active Web verification failed")
        passed = True
        report["result"] = "PATCHED_AND_WEB_VERIFIED"
        print("PHASE170_R3R9_RESULT=PATCHED_AND_WEB_VERIFIED", flush=True)
        print("PHASE170_R3R9_FULL_PYTEST=False", flush=True)
        return 0
    except Exception as exc:
        report["result"] = "REFUSED_OR_ROLLED_BACK"
        report["error"] = repr(exc)
        print(f"PHASE170_R3R9_REFUSED={type(exc).__name__}: {exc}", flush=True)
        return 2
    finally:
        if not passed:
            for target in modified:
                (root / target).write_bytes(saved[target])
                print("PHASE170_R3R9_RESTORED=" + target, flush=True)
        report_path = output / "result.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print("PHASE170_R3R9_REPORT=" + str(report_path), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
