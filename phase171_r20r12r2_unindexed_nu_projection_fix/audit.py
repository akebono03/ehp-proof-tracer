"""Re-run the existing canonical R20R12 public-search and narrative audit."""
from __future__ import annotations

import json
from pathlib import Path

from phase171_r20r12_verified_cyclic_narrative.audit import run as run_previous_audit

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
PREVIOUS_OUTPUT = HERE.parent / "phase171_r20r12_verified_cyclic_narrative" / "output"


def run() -> dict[str, object]:
    original = run_previous_audit()
    if not original.get("public_complete"):
        raise RuntimeError("public proof became incomplete")
    if not original.get("root_order_four_ancestry_verified"):
        raise RuntimeError("root order-four ancestry is not verified")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = dict(original)
    report["correction"] = "171-R20R12R2_UNINDEXED_NU_PRIME_PROJECTION"
    report["math_inference_modified"] = False
    report["renderer_modified_by_correction"] = False
    report["web_visual_check_performed"] = False
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    markdown = (PREVIOUS_OUTPUT / "web_narrative.md").read_text(encoding="utf-8")
    (OUTPUT / "web_narrative.md").write_text(markdown, encoding="utf-8")
    print("PHASE171_R20R12R2_PUBLIC_COMPLETE=" + str(report["public_complete"]), flush=True)
    print("PHASE171_R20R12R2_ORDER_FOUR=" + str(report["root_order_four_ancestry_verified"]), flush=True)
    print("PHASE171_R20R12R2_OUTPUT=" + str(OUTPUT / "audit.json"), flush=True)
    print("PHASE171_R20R12R2_RESULT=PASS_RENDERER_AUDIT", flush=True)
    return report


if __name__ == "__main__":
    run()
