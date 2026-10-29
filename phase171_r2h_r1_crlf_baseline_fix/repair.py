"""Guarded repair of the R2H installer's CRLF/LF preflight comparison.

This repairs only files from the previously distributed R2H folder. It does
not modify tracked application source, Git history, or unrelated worktrees.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
FILES = (
    (
        "phase171_r2h_prop22_cited_hopf/install.py",
        "install_FULL.py",
        "0d370f801fb9528cd3a05f522d32a8803bbe8822874ccfe34afd5a48f6c8c8b6",
        "988ae78111f85f179eb4bf1104e786ab3e4dc0bacbb5080e6a22e14910a65ec4",
    ),
    (
        "phase171_r2h_prop22_cited_hopf/tests/test_install.py",
        "test_install_FULL.py",
        "c9826bf3d94a34e9be55115ee05877c3d26cfebdb37db681e5c8210e7b4fe058",
        "b14049db4c23886a70df1195adc992bcbc10afc732250f6488acd3e825df5508",
    ),
)


def inspect() -> tuple[tuple[str, Path, bytes, bytes], ...]:
    """Return only independently hash-validated, recognized file states."""
    verified = []
    for relative, payload, original_sha, patched_sha in FILES:
        target = ROOT / relative
        replacement = PACKAGE / payload
        if not target.is_file() or not replacement.is_file():
            raise FileNotFoundError(relative + " or " + payload)
        current = target.read_bytes()
        new_data = replacement.read_bytes()
        if sha256(new_data).hexdigest() != patched_sha:
            raise RuntimeError("repair payload hash mismatch: " + relative)
        actual = sha256(current).hexdigest()
        if actual == original_sha:
            state = "NEEDS_REPAIR"
        elif actual == patched_sha:
            state = "ALREADY_REPAIRED"
        else:
            raise RuntimeError("unreviewed R2H installer content: " + relative)
        verified.append((state, target, current, new_data))
    return tuple(verified)


def run(mode: str) -> int:
    """Read-only check or backed-up, strictly scoped replacement."""
    if mode not in ("check", "apply"):
        raise ValueError("mode must be check or apply")
    items = inspect()
    for state, target, _, _ in items:
        print("PHASE171_R2H_R1_PREFLIGHT=" + str(target.relative_to(ROOT)) + ":" + state, flush=True)
    if mode == "check":
        print("PHASE171_R2H_R1_RESULT=PASS_CHECK", flush=True)
        return 0
    pending = tuple(item for item in items if item[0] == "NEEDS_REPAIR")
    if pending:
        root = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
        backup_root = root / ("phase171_r2h_r1_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        backup_root.mkdir(parents=True, exist_ok=False)
        for _, target, original, _ in pending:
            destination = backup_root / target.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, destination)
            if destination.read_bytes() != original:
                raise RuntimeError("backup verification failed: " + str(target))
        print("PHASE171_R2H_R1_BACKUP=" + str(backup_root), flush=True)
        for _, target, original, new_data in pending:
            if target.read_bytes() != original:
                raise RuntimeError("installer file changed after backup: " + str(target))
            target.write_bytes(new_data)
            if target.read_bytes() != new_data:
                raise RuntimeError("installer repair write verification failed: " + str(target))
            print("PHASE171_R2H_R1_PATCHED=" + str(target.relative_to(ROOT)), flush=True)
    checked = inspect()
    if any(state != "ALREADY_REPAIRED" for state, _, _, _ in checked):
        raise RuntimeError("R2H installer repair did not reach the expected state")
    print("PHASE171_R2H_R1_RESULT=PASS_APPLY", flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "apply"))
    args = parser.parse_args()
    try:
        return run(args.mode)
    except (RuntimeError, ValueError, OSError) as exc:
        print("PHASE171_R2H_R1_ERROR=" + f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    sys.exit(main())
