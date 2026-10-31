"""Read-only result aggregation after the corrected R20R13R2 audit."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    input_path = (
        ROOT / "phase171_r20r13r2_multiple_blank_eta_merge" / "output" / "audit.json"
    )
    report = json.loads(input_path.read_text(encoding="utf-8"))
    if (report.get("public_status") != "complete"
            or report.get("exact_three_eta_grouped") is not True
            or report.get("reference_count") != 8):
        raise RuntimeError("the corrected three-equation layout did not pass")
    output = HERE / "output"
    output.mkdir(parents=True, exist_ok=True)
    summary = {
        "phase": "171-R20R13R3",
        "correction": "HEAD CONTENT GUARD REPLACES EXACT COMMIT PIN",
        "source_guard": "reviewed git HEAD and worktree content",
        "public_status": report["public_status"],
        "exact_three_eta_grouped": report["exact_three_eta_grouped"],
        "reference_count": report["reference_count"],
        "production_math_modified": False,
        "renderer_modified": False,
        "full_pytest": False,
    }
    (output / "audit.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("PHASE171_R20R13R3_PUBLIC_STATUS=" + report["public_status"])
    print("PHASE171_R20R13R3_ETA_GROUPED_THREE=True")
    print("PHASE171_R20R13R3_REFERENCES=8")
    print("PHASE171_R20R13R3_RESULT=PASS_CONTENT_GUARDED_ETA_LAYOUT")


if __name__ == "__main__":
    main()
