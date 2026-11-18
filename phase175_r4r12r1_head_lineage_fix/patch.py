"""R4R12R1: correct reviewed HEAD without rewriting prior audit evidence."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess

OLD = "abf619040d52aa9fd61c5bca60db81e28912e24d"
NEW = "344fc101fdfcce49ec80f867f80a0614d96c214e"
PACKAGE = Path("phase175_r4r12_public_two_summand_quotient")
COMMITTED_PRODUCTION_BLOB = "725d2227caa3544aad9288309231a8f7e33619f0"


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True,
                            text=True, encoding="utf-8", check=False)
    if result.returncode:
        raise RuntimeError("R4R12R1_GIT_FAILURE: " + " ".join(args))
    return result.stdout.strip()


def replacement_paths(root: Path) -> tuple[Path, Path]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("R4R12R1_WRONG_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R4R12R1_WRONG_BRANCH")
    if git(root, "rev-parse", "HEAD") != NEW:
        raise RuntimeError("R4R12R1_UNREVIEWED_HEAD")
    if subprocess.run(["git", "merge-base", "--is-ancestor", OLD, NEW],
                      cwd=root, check=False).returncode != 0:
        raise RuntimeError("R4R12R1_UNREVIEWED_LINEAGE")
    changed = git(root, "diff", "--name-only").splitlines()
    changed += git(root, "diff", "--cached", "--name-only").splitlines()
    if any(p != "phase165_r52_r9_shared_math.py" for p in changed):
        raise RuntimeError("R4R12R1_UNREVIEWED_TRACKED_CHANGE")
    return root / PACKAGE / "installer.py", root / PACKAGE / "audit.py"


def patch_text(installer: str, audit: str) -> tuple[str, str]:
    assignment_old = 'HEAD = "' + OLD + '"'
    assignment_new = 'HEAD = "' + NEW + '"'
    if installer.count(assignment_old) == 1:
        new_installer = installer.replace(assignment_old, assignment_new, 1)
    elif installer.count(assignment_new) == 1:
        new_installer = installer
    else:
        raise RuntimeError("R4R12R1_UNEXPECTED_INSTALLER_HEAD")
    old_base_check = 'git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != previous.BASE_WORKING_BLOB'
    new_base_check = ('git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != '
                      + repr(COMMITTED_PRODUCTION_BLOB))
    if new_installer.count(old_base_check) == 1:
        new_installer = new_installer.replace(old_base_check, new_base_check, 1)
    elif new_installer.count(new_base_check) != 1:
        raise RuntimeError("R4R12R1_UNEXPECTED_BASE_PRODUCTION_GUARD")
    # Only the R4R11 prior *report* must retain the historical HEAD.
    original = 'not isinstance(before, dict) or before.get("head") != HEAD'
    corrected = 'not isinstance(before, dict) or before.get("head") != "' + OLD + '"'
    if audit.count(original) == 1:
        new_audit = audit.replace(original, corrected, 1)
    elif audit.count(corrected) == 1:
        new_audit = audit
    else:
        raise RuntimeError("R4R12R1_UNEXPECTED_PRIOR_VALIDATION")
    for label, content in (("installer", new_installer), ("audit", new_audit)):
        ast.parse(content, filename=label + ".py")
    if 'HEAD = installer.HEAD' not in new_audit:
        raise RuntimeError("R4R12R1_AUDIT_HEAD_BINDING_CHANGED")
    if 'if head != HEAD:' not in new_audit:
        raise RuntimeError("R4R12R1_PREFLIGHT_GUARD_CHANGED")
    if 'if git(root, "rev-parse", "HEAD") != HEAD:' not in new_installer:
        raise RuntimeError("R4R12R1_INSTALL_GUARD_CHANGED")
    return new_installer, new_audit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    installer_path, audit_path = replacement_paths(root)
    if not installer_path.is_file() or not audit_path.is_file():
        raise RuntimeError("R4R12R1_R4R12_SOURCE_MISSING")
    data = [p.read_bytes() for p in (installer_path, audit_path)]
    endings = [b"\r\n" if b"\r\n" in item else b"\n" for item in data]
    original = [item.replace(b"\r\n", b"\n").decode("utf-8") for item in data]
    changed = patch_text(*original)
    for path, before, after, eol in zip((installer_path, audit_path), original, changed, endings):
        print("R4R12R1_" + path.name.upper() + "_CHANGE=" + str(before != after))
        if not args.dry_run and before != after:
            result = after.encode("utf-8")
            if eol == b"\r\n":
                result = result.replace(b"\n", b"\r\n")
            path.write_bytes(result)
    print("R4R12R1_GATE=PASS_HEAD_AND_PRIOR_REPORT_PIN_CORRECTION" + ("_DRYRUN" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
