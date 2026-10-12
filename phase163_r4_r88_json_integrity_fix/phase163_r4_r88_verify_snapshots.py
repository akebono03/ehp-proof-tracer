"""Validate R86/R87 inputs against reviewed JSON, independent of formatting."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate_snapshot(actual_path: Path, snapshot_path: Path) -> None:
    """Reject any JSON data change while accepting layout and encoding differences."""
    actual = json.loads(actual_path.read_text(encoding="utf-8-sig"))
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8-sig"))
    if not isinstance(actual, dict) or not isinstance(snapshot, dict):
        raise ValueError("snapshot inputs must be JSON objects")
    if actual != snapshot:
        raise ValueError(f"reviewed JSON data mismatch: {actual_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r86", required=True, type=Path)
    parser.add_argument("--r87", required=True, type=Path)
    parser.add_argument("--snapshot-r86", required=True, type=Path)
    parser.add_argument("--snapshot-r87", required=True, type=Path)
    args = parser.parse_args()
    validate_snapshot(args.r86, args.snapshot_r86)
    validate_snapshot(args.r87, args.snapshot_r87)
    print("R86 and R87 reviewed JSON data match; formatting differences ignored.")


if __name__ == "__main__":
    main()
