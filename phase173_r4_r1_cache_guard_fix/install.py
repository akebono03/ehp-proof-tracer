"""Guarded update of the untracked Phase 173 R4-R1 read-only audit package.

No Git writes, reset, checkout, clean, or tracked-file modifications occur.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil

from phase173_r4_r1_cache_guard_fix.manifest import ORIGINAL_SHA256

FILES = ("audit.py", "run.ps1", "tests/test_audit.py")
PACKAGE = "phase173_r4_r1_audit_only"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def replacement_plan(root: Path, package: Path) -> tuple[str, ...]:
    """Fail closed unless all targets are known original or known corrected bytes."""
    states = []
    for relative in FILES:
        target = root / PACKAGE / relative
        updated = package / relative
        if not target.is_file() or not updated.is_file():
            raise RuntimeError("Missing audit component: " + relative)
        current = digest(target)
        if current == ORIGINAL_SHA256[relative]:
            states.append("ORIGINAL")
        elif current == digest(updated):
            states.append("CORRECTED")
        else:
            raise RuntimeError("Unrecognized local modifications; refusing overwrite: " + relative)
    if len(set(states)) != 1:
        raise RuntimeError("Partially updated audit package; refusing automatic changes")
    return tuple(states)


def install(root: Path, package: Path, *, dry_run: bool) -> str:
    states = replacement_plan(root, package)
    if states[0] == "CORRECTED":
        return "ALREADY_INSTALLED"
    if dry_run:
        return "DRY_RUN_VALIDATED_NO_FILES_CHANGED"
    base = Path(os.environ.get("LOCALAPPDATA") or Path.home())
    backup = (base / "EHPProofTracerRecovery" / "phase173_r4_r1_cache_guard_fix"
              / "backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ"))
    backup.mkdir(parents=True, exist_ok=False)
    # Retain exact before-images; refuse modified local copies above.
    for relative in FILES:
        target = backup / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / PACKAGE / relative, target)
    manifest = {relative: ORIGINAL_SHA256[relative] for relative in FILES}
    (backup / "original_sha256.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("PHASE173_R4_R1_CACHE_GUARD_BACKUP=" + str(backup))
    for relative in FILES:
        shutil.copy2(package / relative, root / PACKAGE / relative)
    if replacement_plan(root, package) != ("CORRECTED",) * len(FILES):
        raise RuntimeError("Corrected audit package content verification failed")
    return "INSTALLED_UNTRACKED_AUDIT_PACKAGE_ONLY"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    package = Path(__file__).resolve().parent / "payload" / PACKAGE
    print("PHASE173_R4_R1_CACHE_GUARD=" + install(root, package, dry_run=args.dry_run))
    print("PHASE173_R4_R1_NO_GIT_MUTATION=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
