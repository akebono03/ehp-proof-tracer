import json
from pathlib import Path
from phase165_r14_r10_premise_audit import audit_summary

def main():
    report = audit_summary()
    output = Path("phase165_r14_r10_output")
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    (output / "report.md").write_text("# Phase 165 R14-R10 — 前提監査\n\n" +
        "\n".join(f"- {r['label']}: {r['reason']}" for r in report["obligations"]) + "\n", encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
