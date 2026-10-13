from pathlib import Path
import json
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r4_remaining_schemas import audit_remaining_toda51

def main():
    bridge, _ = build_phase165_r5_manifest_bridge()
    report = audit_remaining_toda51(bridge)
    out = Path("phase165_r14_r4_output")
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "report.md").write_text(
        "# Phase 165 R14-R4 監査\n\n" +
        "\n".join(f"- {k}: {v}" for k,v in report.items()) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
