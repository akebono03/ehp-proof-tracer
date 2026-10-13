import json
from pathlib import Path
from phase165_r14_r22_same_reference import audit_r22


def main():
    report=audit_r22(Path(__file__).with_name("toda_51_complete.tex"))
    target=Path("phase165_r14_r22_output")
    target.mkdir(exist_ok=True)
    (target/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
