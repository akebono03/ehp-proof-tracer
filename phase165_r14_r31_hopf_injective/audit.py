import json
from pathlib import Path
from phase165_r14_r31_hopf_injective import audit_r31

def main():
    report=audit_r31(Path(__file__).with_name("toda_51_complete.tex"))
    out=Path("phase165_r14_r31_output")
    out.mkdir(exist_ok=True)
    (out/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
