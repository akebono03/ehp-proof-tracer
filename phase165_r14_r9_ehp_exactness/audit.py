from pathlib import Path
import json
from phase165_r14_r9_ehp_exactness import audit_pi32_hopf_exactness

def main():
    report = audit_pi32_hopf_exactness()
    folder = Path("phase165_r14_r9_output")
    folder.mkdir(exist_ok=True)
    (folder/"report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    (folder/"report.md").write_text("# Phase 165 R14-R9 監査\n\n" +
        "\n".join(f"- {k}: {v}" for k,v in report.items()) + "\n", encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
