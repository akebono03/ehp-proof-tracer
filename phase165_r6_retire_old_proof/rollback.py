from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    report = args.report.resolve()
    root = args.root.resolve()
    data = json.loads(report.read_text(encoding="utf-8"))
    for item in data["manifest"]:
        if item["path"] not in data["removed"]:
            continue
        original = root / item["path"]
        source = report.parent / "backup" / item["path"]
        blob = source.read_bytes()
        if hashlib.sha256(blob).hexdigest() != item["sha256"]:
            raise RuntimeError("Backup hash mismatch: " + item["path"])
        if original.exists():
            raise RuntimeError("Refusing to overwrite: " + item["path"])
        original.parent.mkdir(parents=True, exist_ok=True)
        original.write_bytes(blob)
        print("Restored", item["path"])
if __name__ == "__main__":
    main()
