"""Guarded, idempotent two-file repair of the R2F audit's root variable.

This installer never invokes checkout/reset or changes application proof code.
Only pre-reviewed original R2F audit files or already-repaired files are accepted.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import os
from pathlib import Path
import sys
import tempfile
import traceback


REPO = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class PatchSpec:
    relative_target: str
    full_source_name: str
    original_sha256: str
    updated_sha256: str


PATCHES = (
    PatchSpec(
        "phase171_r2f_pi63_extension_gap_audit/audit.py",
        "audit_FULL.py",
        "350e32844dd24b73ccde87e2a7ca2da8060e62f8ded794759e05737c66320ae4",
        "6ad8575297dcb7689a3f19f1fedf0992dae3c106cd7502d74062b56e466d3756",
    ),
    PatchSpec(
        "phase171_r2f_pi63_extension_gap_audit/tests/test_audit.py",
        "test_audit_FULL.py",
        "aa55bfee677b65f65a03514d747c449524dcf096069da6157e686e2720a51044",
        "f8fff0efd46771ff4e6cd09eb86a62dc981e56e2ff615a134641d3a4f0330e64",
    ),
)


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def preflight(repo: Path = REPO, package: Path = PACKAGE) -> tuple[dict, ...]:
    """Reject modified user files and invalid bundle templates before any write."""
    reviewed = []
    for spec in PATCHES:
        target = repo / spec.relative_target
        source = package / spec.full_source_name
        if not target.is_file() or not source.is_file():
            raise RuntimeError("required R2F audit/repair file missing: " + spec.relative_target)
        payload = source.read_bytes()
        if digest(payload) != spec.updated_sha256:
            raise RuntimeError("repair template checksum mismatch: " + spec.relative_target)
        previous = target.read_bytes()
        current_hash = digest(previous)
        if current_hash == spec.original_sha256:
            state = "NEEDS_REPAIR"
        elif current_hash == spec.updated_sha256:
            state = "ALREADY_REPAIRED"
        else:
            raise RuntimeError(
                "unrecognized local edits; refusing to overwrite: " + spec.relative_target
            )
        reviewed.append({
            "target": target,
            "source": source,
            "previous": previous,
            "updated": payload,
            "original_sha256": current_hash,
            "spec": spec,
            "state": state,
        })
    return tuple(reviewed)


def atomic_replace(path: Path, payload: bytes) -> None:
    """Write one verified template atomically; preserve existing content on failure."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".r2f_r1_", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def apply(repo: Path = REPO, package: Path = PACKAGE) -> None:
    """Backup exact originals outside the repo and repair only matching audit files."""
    reviewed = preflight(repo, package)
    changes = [entry for entry in reviewed if entry["state"] == "NEEDS_REPAIR"]
    if not changes:
        print("PHASE171_R2F_R1_ALREADY_REPAIRED=True", flush=True)
        return
    backup_parent = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    backup = backup_parent / (
        "phase171_r2f_r1_fix_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    )
    backup.mkdir(parents=True, exist_ok=False)
    # Finish backups before touching any target.
    for entry in changes:
        name = str(entry["spec"].relative_target).replace("/", "__")
        path = backup / (name + ".before")
        path.write_bytes(entry["previous"])
        if digest(path.read_bytes()) != entry["original_sha256"]:
            raise RuntimeError("failed to verify backup: " + str(path))
    written = []
    try:
        for entry in changes:
            target = entry["target"]
            if digest(target.read_bytes()) != entry["original_sha256"]:
                raise RuntimeError("concurrent edit detected; refusing to replace: " + str(target))
            atomic_replace(target, entry["updated"])
            if digest(target.read_bytes()) != entry["spec"].updated_sha256:
                raise RuntimeError("repair write verification failed: " + str(target))
            written.append(entry)
    except Exception:
        # Restore only files still matching the bytes we just installed.
        for entry in reversed(written):
            target = entry["target"]
            if digest(target.read_bytes()) == entry["spec"].updated_sha256:
                atomic_replace(target, entry["previous"])
        raise
    print("PHASE171_R2F_R1_BACKUP=" + str(backup), flush=True)
    for entry in changes:
        print("PHASE171_R2F_R1_PATCHED=" + entry["spec"].relative_target, flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "apply"))
    args = parser.parse_args()
    try:
        reviewed = preflight()
        for entry in reviewed:
            print("PHASE171_R2F_R1_PREFLIGHT=" + entry["spec"].relative_target
                  + ":" + entry["state"], flush=True)
        if args.action == "apply":
            apply()
        print("PHASE171_R2F_R1_RESULT=PASS_" + args.action.upper(), flush=True)
        return 0
    except Exception as exc:
        print("PHASE171_R2F_R1_ERROR=" + f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        print(traceback.format_exc()[-2200:], file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
