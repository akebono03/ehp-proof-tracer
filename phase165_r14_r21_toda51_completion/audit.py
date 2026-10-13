import json
from pathlib import Path
from phase165_r14_r21_toda51_completion import audit_r21

def main():
    data = audit_r21(Path(__file__).with_name("toda_51_complete.tex"))
    folder = Path("phase165_r14_r21_output")
    folder.mkdir(exist_ok=True)
    (folder/"report.json").write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
