from __future__ import annotations

import json
from pathlib import Path

from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r6_binding_candidates import inventory_typed_source_bindings


def main():
    bridge, summary = build_phase165_r5_manifest_bridge(
        Path("phase163_r4_r94_output/manifest.json")
    )
    report = inventory_typed_source_bindings(bridge)
    output = Path("phase165_r6_output")
    output.mkdir(exist_ok=True)
    payload = {
        "phase": "165 R6",
        "mode": "NON_PROMOTING_TYPED_SOURCE_CANDIDATES",
        "source_assertions": summary.source_assertion_count,
        "existing_typed_or_fixed_assertions": summary.existing_assertion_count,
        "unique_locator_candidate_count": len(report.candidates),
        "unmatched_source_count": len(report.unmatched_source_ids),
        "ambiguous_source_count": len(report.ambiguous_source_ids),
        "typed_without_source_count": len(report.typed_without_source_ids),
        "newly_proof_eligible": report.proof_eligible_count,
        "proof_links": len(bridge.proof_links),
        "pi5_3_proved": False,
        "full_pytest_run": False,
        "candidates": [vars(item) for item in report.candidates],
        "ambiguous_source_ids": list(report.ambiguous_source_ids),
        "unmatched_source_ids": list(report.unmatched_source_ids),
    }
    (output / "report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = ["# Phase 165 R6 — 命題対応候補", "", "文献番号一致だけでは証明使用資格を認めない。", ""]
    for key in ("source_assertions", "existing_typed_or_fixed_assertions",
                "unique_locator_candidate_count", "ambiguous_source_count",
                "unmatched_source_count", "newly_proof_eligible"):
        lines.append(f"- {key}: {payload[key]}")
    lines += ["", "## 要確認の対応候補", ""]
    for item in report.candidates:
        lines.append(f"- `{item.source_assertion_id}` → `{item.typed_assertion_id}` ({item.locator})")
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({key: val for key, val in payload.items()
                      if not isinstance(val, list)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
