"""Initial baseline capture. Never overwrites an existing golden file."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from phase165_r4_golden_baseline.golden import CASES, BASE, baseline_path, capture, verify_all


def main() -> None:
    BASE.mkdir(exist_ok=True)
    existing = [str(baseline_path(name)) for name, _, _ in CASES if baseline_path(name).exists()]
    if existing:
        if len(existing) != len(CASES):
            raise RuntimeError("Partial baseline set: inspect before proceeding; no overwrite performed")
        verify_all()
        print("R4 existing baselines verified; no files rewritten")
        return
    records = [capture(name, n, k) for name, n, k in CASES]
    for record in records:
        path = baseline_path(record["case"])
        with path.open("x", encoding="utf-8", newline="\n") as f:
            json.dump(record, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Frozen baseline:", path, record["markdown_sha256"])
    verify_all()
    print("R4 golden baseline capture PASS")


if __name__ == "__main__":
    main()
