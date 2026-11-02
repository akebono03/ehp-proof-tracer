"""Re-run the already reviewed R4-R7 isolated proof search on the corrected context."""
from __future__ import annotations

import json
from pathlib import Path

from phase173_r4_r7_source_first_rule.audit import inspect_live


def verify(root: Path) -> dict:
    rows = inspect_live(root)
    if len(rows) != 3 or [row.get("dimension") for row in rows] != [8, 9, 10]:
        raise RuntimeError("unexpected Toda (5.6) isolated target set")
    for row in rows:
        print(
            "PHASE173_R4_R7R2_" + row["group"] +
            " STATUS=" + str(row["isolated_status"]) +
            " ROOT_CERTIFIED=" + str(row["root_certified"]) +
            " OPEN=" + str(row.get("open_goals")) +
            " STEPS=" + str(row.get("proven_steps")),
            flush=True,
        )
    result = {
        "phase": "173 R4-R7R2", "mode": "ISOLATED_SEARCH_ONLY",
        "public_connection_changed": False,
        "results": rows,
        "all_three_certified": all(
            row["typed_generator_match"]
            and row["source_first"]
            and row["proposals"] == 1
            and row["isolated_status"] == "complete"
            and row["root_certified"]
            and row.get("open_goals") == 0
            for row in rows
        ),
    }
    if not result["all_three_certified"]:
        print("PHASE173_R4_R7R2_ALL_ISOLATED_CERTIFIED=False", flush=True)
        return result
    print("PHASE173_R4_R7R2_ALL_ISOLATED_CERTIFIED=True", flush=True)
    return result


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    result = verify(root)
    output = root / "phase173_r4_r7r2_pi84_prior_selection" / "verification_result.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE173_R4_R7R2_REPORT=" + str(output), flush=True)
    return 0 if result["all_three_certified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
