from __future__ import annotations
import json
from pathlib import Path
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r2_toda51 import TODA_51_SCHEMAS, instantiate_toda51_clause, report_toda51_source


def main() -> None:
    bridge, _ = build_phase165_r5_manifest_bridge()
    report = report_toda51_source(bridge)
    report["phase"] = "165 R14-R2"
    report["typed_examples"] = [
        repr(instantiate_toda51_clause(TODA_51_SCHEMAS[0], 2)),
        repr(instantiate_toda51_clause(TODA_51_SCHEMAS[1], 1)),
        repr(instantiate_toda51_clause(TODA_51_SCHEMAS[1], 3)),
    ]
    output = Path("phase165_r14_r2_output")
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "report.md").write_text("# Phase 165 R14-R2 — Toda (5.1) typed clauses\n\n" + "\n".join(f"- {k}: {v}" for k, v in report.items()) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
