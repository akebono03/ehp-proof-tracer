"""Summarize the existing R6 static dependency audit; no code changes."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    records = data["test_dependencies"]
    statuses = Counter(record["classification"] for record in records)
    direct = []
    indirect = []
    unresolved = []
    for record in records:
        route = record["path_to_legacy_probe"]
        if route is None:
            unresolved.append(record["test_path"])
        elif len(route) == 2:
            direct.append(record["test_path"])
        else:
            indirect.append(record)
    summary = {
        "phase": "165 R6-8",
        "status": "DEPENDENCY_CLASSIFICATION_ONLY",
        "target_error_records": len(records),
        "classification_counts": dict(statuses),
        "direct_importers": direct,
        "indirect_example_chains": indirect[:12],
        "unresolved_test_paths": unresolved,
        "source_modified": False,
        "tests_deleted": False,
        "full_pytest_run": False,
        "notes": [
            "Static AST dependency chains do not establish the runtime cause on their own.",
            "A missing path does not prove that a test is obsolete.",
            "Do not restore removed group-specific inference rules to satisfy imports.",
        ],
    }
    out = path.with_name("r6_8_summary.json")
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("R6-8 target error records:", len(records))
    print("Confirmed static chains:", statuses.get("PROVEN_STATIC_CHAIN", 0))
    print("Unresolved static chains:", statuses.get("UNRESOLVED_STATIC_CHAIN", 0))
    print("Direct test-to-probe imports:", len(direct))
    print("Indirect chains:", len(indirect))
    for item in indirect[:5]:
        print("CHAIN:", " -> ".join(item["path_to_legacy_probe"]))
    print("Summary:", out)
    return 0 if records else 1


if __name__ == "__main__":
    raise SystemExit(main())
