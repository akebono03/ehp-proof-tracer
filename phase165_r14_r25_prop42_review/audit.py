import json
from pathlib import Path
from phase165_r14_r25_prop42_review import audit_r25, render_report

def main():
    report=audit_r25()
    folder=Path("phase165_r14_r25_output")
    folder.mkdir(exist_ok=True)
    (folder/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    (folder/"report.md").write_text(render_report(report),encoding="utf8")
    public={k:v for k,v in report.items() if k!="source_reviews"}
    print(json.dumps(public,ensure_ascii=False,indent=2))
    print("Raw Proposition 4.2 source: phase165_r14_r25_output/report.md")

if __name__=="__main__":
    main()
