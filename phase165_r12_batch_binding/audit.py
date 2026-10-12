from __future__ import annotations

import json
from pathlib import Path

from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r12_typed_binding import build_batch_typed_bindings


def main() -> None:
    bridge, _ = build_phase165_r5_manifest_bridge()
    result = build_batch_typed_bindings(bridge)
    report = {
        "phase": "165 R12",
        "mode": "BATCH_ADOPTED_TEX_SOURCE_BINDING_NOT_MATH_CERTIFICATION",
        "source_assertions": len(result.records),
        "unique_locator_candidates": result.unique_candidates,
        "ambiguous_locator_candidates": result.ambiguous_candidates,
        "unmatched_source_assertions": result.unmatched,
        "mathematically_typed_assertions": result.mathematically_typed,
        "newly_proof_eligible": result.proof_eligible,
        "pi5_3_proved": False,
        "full_pytest_run": False,
    }
    output = Path("phase165_r12_output")
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 165 R12 — 一括 TeX 主張記録と型付き候補\n\n"
        + "\n".join(f"- {k}: {v}" for k, v in report.items()) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
