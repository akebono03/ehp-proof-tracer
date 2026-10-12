"""Run the Phase 165 R5 production bridge audit."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge


def main() -> None:
    bridge, summary = build_phase165_r5_manifest_bridge()
    report = {
        "phase": "165 R5",
        "mode": "SOURCE_ORDER_BRIDGE_ONLY",
        "source_references_connected": summary.source_reference_count,
        "source_assertions_connected": summary.source_assertion_count,
        "existing_assertions_preserved": summary.existing_assertion_count,
        "proof_links_preserved": summary.proof_link_count,
        "newly_proof_eligible": summary.newly_eligible_count,
        "verified_typed_statement_binding": False,
        "inference_catalog_connected": False,
        "pi5_3_proved": False,
        "full_pytest_run": False,
    }
    out = Path("phase165_r5_output")
    out.mkdir(exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "report.md").write_text(
        "# Phase 165 R5 — 文献掲載順の接続\n\n" +
        "\n".join(f"- {k}: {v}" for k, v in report.items()) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
