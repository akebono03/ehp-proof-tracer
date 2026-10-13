import json
from pathlib import Path
from phase165_r14_r19_registry_gate import audit_r19

def main():
    result=audit_r19()
    out=Path("phase165_r14_r19_output")
    out.mkdir(exist_ok=True)
    (out/"report.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    (out/"report.md").write_text("# Phase 165 R14-R19\n\n" +
        "\n".join(f"- {k}: {v}" for k,v in result.items())+"\n",encoding="utf8")
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
