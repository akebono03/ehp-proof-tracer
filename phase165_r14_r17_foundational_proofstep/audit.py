import json
from pathlib import Path
from phase165_r14_r17_foundational_proofstep import audit_r17


def main():
    report = audit_r17()
    output = Path("phase165_r14_r17_output")
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
