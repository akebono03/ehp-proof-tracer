import json
from pathlib import Path
import sys
from phase165_r14_r27_scope_delta import audit_r27

def main():
    path=Path(sys.argv[1]) if len(sys.argv)>1 else None
    report=audit_r27(path)
    out=Path("phase165_r14_r27_output")
    out.mkdir(exist_ok=True)
    (out/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps({k:v for k,v in report.items() if k!="context_excerpt"},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
