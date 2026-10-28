"""Apply or restore the one R10A projection function with byte-exact backups."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from .patch import TARGET, transform


def apply(root: Path, output: Path) -> None:
    source = root / TARGET
    before_path = output / "projection.py.before"
    after_path = output / "projection.py.FULL"
    full_function_path = output / "project_verified_stable_image_chain_FULL.py"
    if before_path.exists() or after_path.exists():
        raise RuntimeError("R10EJ output already contains a previous installation")
    original = source.read_bytes()
    modified, full_function = transform(original)
    output.mkdir(parents=True, exist_ok=True)
    before_path.write_bytes(original)
    after_path.write_bytes(modified)
    full_function_path.write_text(full_function, encoding="utf-8")
    try:
        if source.read_bytes() != original:
            raise RuntimeError("R10EJ target changed between backup and patch")
        source.write_bytes(modified)
        if source.read_bytes() != modified:
            raise RuntimeError("R10EJ edited target did not match reviewed patch")
    except BaseException:
        source.write_bytes(original)
        raise
    print("R10EJ_PATCHED=" + str(source), flush=True)
    print("R10EJ_RESTORE_BACKUP=" + str(before_path), flush=True)
    print("R10EJ_FULL_FUNCTION=" + str(full_function_path), flush=True)
    print("R10EJ_TARGET_HASH=" + hashlib.sha256(modified).hexdigest(), flush=True)


def restore(root: Path, output: Path) -> None:
    source = root / TARGET
    saved = output / "projection.py.before"
    if not saved.is_file():
        raise FileNotFoundError("R10EJ cannot restore without the original backup")
    original = saved.read_bytes()
    source.write_bytes(original)
    if source.read_bytes() != original:
        raise RuntimeError("R10EJ byte-exact restore verification failed")
    print("R10EJ_ROLLBACK=source restored byte-for-byte", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("apply", "restore"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "apply":
        apply(args.root, args.output)
    else:
        restore(args.root, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
