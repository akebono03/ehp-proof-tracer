"""Read-only installed Web smoke verification; phase-wide tests are excluded."""
from __future__ import annotations

import json
from pathlib import Path

from web_group_proof import build_standard_web_group_proof_view


def main() -> int:
    rows = []
    for dimension in (7, 8, 9, 10, 11):
        view = build_standard_web_group_proof_view(
            n=4, k=dimension - 4, mode="narrative", citation_source="model",
        )
        math = [segment.value for line in view.rendered_lines for segment in line.segments
                if segment.kind in ("inline_math", "display_math")]
        complete = (
            view.key == "generic-complete-proof" and not view.partial_result
            and bool(view.rendered_lines)
            and any(r"\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}" in value for value in math)
            and (dimension == 7 or any(
                rf"\Phi_{{{dimension}}}:" in value for value in math
            ))
        )
        print(
            "PHASE173_R4_R12_PI_" + str(dimension) + "_4"
            + " WEB_COMPLETE=" + str(complete)
            + " WEB_KEY=" + view.key,
            flush=True,
        )
        rows.append({"dimension": dimension, "web_complete": complete, "key": view.key})
    output = Path(__file__).with_name("verification_result.json")
    success = len(rows) == 5 and all(row["web_complete"] for row in rows)
    output.write_text(json.dumps({"phase": "173 R4-R12", "rows": rows,
                                  "all_five": success}, indent=2) + "\n", encoding="utf-8")
    print("PHASE173_R4_R12_ALL_FIVE_WEB_COMPLETE=" + str(success), flush=True)
    return 0 if success else 2


if __name__ == "__main__":
    raise SystemExit(main())
