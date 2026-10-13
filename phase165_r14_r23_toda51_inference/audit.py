import json
from pathlib import Path
from phase165_r14_r23_toda51_inference import audit_r23

def main():
    report = audit_r23(Path(__file__).with_name("toda_51_complete.tex"))
    output = Path("phase165_r14_r23_output")
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
