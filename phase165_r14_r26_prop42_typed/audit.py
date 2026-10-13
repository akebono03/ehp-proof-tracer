import json
from pathlib import Path
from phase165_r14_r26_prop42_typed import audit_r26

def main():
    r=audit_r26()
    o=Path("phase165_r14_r26_output")
    o.mkdir(exist_ok=True)
    (o/"report.json").write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(r,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
