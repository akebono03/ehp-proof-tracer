"""R4R12R1R2: restore the historical R4R11 HEAD in the test fixture only."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess

CURRENT_HEAD = "344fc101fdfcce49ec80f867f80a0614d96c214e"
PRIOR_REPORT_HEAD = "abf619040d52aa9fd61c5bca60db81e28912e24d"
TARGET = Path("phase175_r4r12_public_two_summand_quotient/tests/test_audit.py")
OLD_FIXTURE = '"preflight": {"head": audit.HEAD},'
NEW_FIXTURE = '"preflight": {"head": "' + PRIOR_REPORT_HEAD + '"},'


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, check=False, capture_output=True,
        encoding="utf-8", errors="replace", text=True,
    )
    if result.returncode:
        raise RuntimeError("R4R12R1R2_GIT_FAILED: " + " ".join(args))
    return result.stdout.strip()


def checked_paths(root: Path) -> Path:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("R4R12R1R2_WRONG_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R4R12R1R2_WRONG_BRANCH")
    if git(root, "rev-parse", "HEAD") != CURRENT_HEAD:
        raise RuntimeError("R4R12R1R2_UNREVIEWED_HEAD")
    check = subprocess.run(
        ["git", "merge-base", "--is-ancestor", PRIOR_REPORT_HEAD, CURRENT_HEAD],
        cwd=root, check=False, capture_output=True,
    )
    if check.returncode:
        raise RuntimeError("R4R12R1R2_LINEAGE_NOT_REVIEWED")
    changed = sorted(set(
        git(root, "diff", "--name-only").splitlines()
        + git(root, "diff", "--cached", "--name-only").splitlines()
    ))
    allowed = {"phase165_r52_r9_shared_math.py", ".pytest_cache/v/cache/nodeids"}
    unknown = sorted(set(changed) - allowed)
    if unknown:
        raise RuntimeError("R4R12R1R2_UNREVIEWED_TRACKED_CHANGE: " + repr(unknown))
    print("R4R12R1R2_TRACKED_CHANGED=" + repr(changed))
    return root / TARGET


def patch_fixture(source: str) -> str:
    """Replace one fixture entry, refusing unreviewed test contents."""
    parsed = ast.parse(source)
    functions = [item for item in parsed.body if isinstance(item, ast.FunctionDef)]
    if not any(item.name == "prior_success_report" for item in functions):
        raise RuntimeError("R4R12R1R2_PRIOR_FIXTURE_FUNCTION_MISSING")
    if not any(item.name == "test_prior_success_is_not_a_root_proof_certificate" for item in functions):
        raise RuntimeError("R4R12R1R2_PRIOR_CERTIFICATE_TEST_MISSING")
    if source.count(OLD_FIXTURE) == 1:
        updated = source.replace(OLD_FIXTURE, NEW_FIXTURE, 1)
    elif source.count(NEW_FIXTURE) == 1 and OLD_FIXTURE not in source:
        updated = source
    else:
        raise RuntimeError("R4R12R1R2_UNREVIEWED_FIXTURE_BODY")
    ast.parse(updated)
    if updated.count(NEW_FIXTURE) != 1:
        raise RuntimeError("R4R12R1R2_FIXTURE_CARDINALITY_CHANGED")
    return updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    target = checked_paths(args.root.resolve())
    if not target.is_file():
        raise RuntimeError("R4R12R1R2_TEST_FILE_NOT_FOUND")
    before = target.read_bytes()
    eol = b"\r\n" if b"\r\n" in before else b"\n"
    normalized = before.replace(b"\r\n", b"\n").decode("utf-8")
    updated = patch_fixture(normalized)
    changed = normalized != updated
    if changed and not args.dry_run:
        payload = updated.encode("utf-8")
        if eol == b"\r\n":
            payload = payload.replace(b"\n", b"\r\n")
        target.write_bytes(payload)
    print("R4R12R1R2_PRIOR_FIXTURE_PATCH_REQUIRED=" + str(changed))
    print("R4R12R1R2_GATE=PASS_PRIOR_REPORT_FIXTURE_CORRECTED" + ("_DRYRUN" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
