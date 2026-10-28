"""Guarded installation with automatic two-file rollback and focused checks."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HEAD = "970535190e160e9f2ae9e596a3ccb13abb9c913c"
REVIEWED_COMMITTED_R3R5_BLOB = "b3e104857e3a8129fb01df65ce3a38ff188ecd1f"
ORIGINAL_REGISTRATION_BLOB = "61b13a6c486132fea1fd4a0e9fcd56b86ce98cff"
PATCHED_R3R5_SHA256 = "52a89e1ab91313c33d36253d1ce67075154503934ad5fe83d5fdf08916230afe"
REGISTRATION = "phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py"
NEW_SOURCE = "phase170_r3_r6_prop58_source.py"
PREVIOUS_PATCH = "phase168_r2_toda52_transport.py"


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=root, text=True, encoding="utf-8",
                          errors="replace", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {proc.stderr.strip()}")
    return proc.stdout.strip()


def preflight(root: Path) -> dict:
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != "develop" or head != HEAD:
        raise RuntimeError(f"unreviewed Git branch or HEAD: {branch} {head}")
    staged = git(root, "diff", "--cached", "--name-only")
    if staged:
        raise RuntimeError("staged tracked changes are not allowed")
    dirty = tuple(x for x in git(root, "diff", "--name-only").splitlines() if x)
    if dirty:
        raise RuntimeError(f"reviewed committed R3-R5 requires clean tracked worktree, found {dirty!r}")
    if git(root, "rev-parse", f"HEAD:{PREVIOUS_PATCH}") != REVIEWED_COMMITTED_R3R5_BLOB:
        raise RuntimeError("reviewed committed R3-R5 Toda (5.2) blob changed")
    if git(root, "rev-parse", f"HEAD:{REGISTRATION}") != ORIGINAL_REGISTRATION_BLOB:
        raise RuntimeError("reviewed registration module blob changed")
    previous = root / PREVIOUS_PATCH
    if hashlib.sha256(previous.read_bytes()).hexdigest() != PATCHED_R3R5_SHA256:
        raise RuntimeError("existing R3-R5 Toda (5.2) implementation changed")
    target = root / REGISTRATION
    if not target.is_file():
        raise RuntimeError("registration module missing")
    source = root / NEW_SOURCE
    if source.exists():
        raise RuntimeError("new source-binding module already exists; refusing overwrite")
    if git(root, "diff", "--", REGISTRATION):
        raise RuntimeError("registration module has preexisting changes")
    return {"branch": branch, "head": head, "committed_r3r5": PREVIOUS_PATCH,
            "committed_r3r5_blob": REVIEWED_COMMITTED_R3R5_BLOB,
            "committed_r3r5_sha256": PATCHED_R3R5_SHA256}


def execute(root: Path, output: Path, key: str, args: list[str]) -> int:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    p = subprocess.run(args, cwd=root, env=env, encoding="utf-8", errors="replace",
                       text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output / f"{key}.log").write_text(p.stdout, encoding="utf-8")
    print(p.stdout, flush=True)
    print(f"PHASE170_R3R6_{key.upper()}_EXIT={p.returncode}", flush=True)
    return p.returncode


def run(root: Path, *, dry_run: bool) -> int:
    package = Path(__file__).resolve().parent
    output_base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery"
    output = output_base / ("phase170_r3_r6_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE170_R3R6_MODE=GUARDED_SOURCE_REGISTRATION", flush=True)
    print(f"PHASE170_R3R6_OUTPUT={output}", flush=True)
    report = {"phase": "170 R3-R6", "mode": "DRY_RUN" if dry_run else "GUARDED_TWO_FILE_PATCH"}
    registration = root / REGISTRATION
    added = root / NEW_SOURCE
    original = None
    applied = False
    succeeded = False
    try:
        report.update(preflight(root))
        original = registration.read_bytes()
        replacement = (package / "replacement" / "phase168_r2_7_4_literature_connection.py").read_bytes()
        source_bytes = (package / "replacement" / NEW_SOURCE).read_bytes()
        compile(replacement, REGISTRATION, "exec")
        compile(source_bytes, NEW_SOURCE, "exec")
        (output / "registration.before.py").write_bytes(original)
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            print("PHASE170_R3R6_DRY_RUN=PASS", flush=True)
            succeeded = True
            return 0
        registration.write_bytes(replacement)
        applied = True
        added.write_bytes(source_bytes)
        selected = [
            package / "tests" / "test_phase170_r3_r6_source.py",
            root / "phase168_r2_7_4_typed_registry_bridge" / "tests" / "test_literature_connection.py",
            root / "phase168_r2_toda52_transport" / "tests" / "test_phase168_r2_toda52_transport.py",
            root / "phase170_r3_r5_toda52_cyclic_generalization" / "tests" / "test_phase170_r3_r5_toda52_cyclic.py",
            root / "tests" / "test_phase167_r3_generic_resolver.py",
        ]
        missing = [str(path) for path in selected if not path.is_file()]
        if missing:
            raise RuntimeError(f"missing reviewed focused tests: {missing}")
        code = execute(root, output, "focused_pytest", [
            sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
            "-p", "no:cacheprovider", *map(str, selected),
        ])
        if code:
            raise RuntimeError(f"focused pytest failed: {code}")
        code = execute(root, output, "active_web", [
            sys.executable, "-B", str(package / "verify.py"),
        ])
        if code:
            raise RuntimeError(f"pi_7^2 Web proof verification failed: {code}")
        report["result"] = "PATCHED_AND_WEB_VERIFIED"
        report["tracked_changed"] = [PREVIOUS_PATCH, REGISTRATION]
        report["new_source"] = NEW_SOURCE
        succeeded = True
        print("PHASE170_R3R6_RESULT=PATCHED_AND_WEB_VERIFIED", flush=True)
        print("PHASE170_R3R6_FULL_PYTEST=False", flush=True)
        return 0
    except Exception as exc:
        report["result"] = "REFUSED_OR_ROLLED_BACK"
        report["error"] = repr(exc)
        print(f"PHASE170_R3R6_REFUSED={type(exc).__name__}: {exc}", flush=True)
        return 2
    finally:
        if applied and not succeeded:
            if original is not None:
                registration.write_bytes(original)
            if added.is_file():
                added.unlink()
            print("PHASE170_R3R6_ROLLBACK=RESTORED_R3R5_STATE", flush=True)
        dest = output / "result.json"
        dest.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"PHASE170_R3R6_REPORT={dest}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
