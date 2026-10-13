import json
from pathlib import Path
from phase165_r14_r28_scope_review import audit_r28


def main():
    report = audit_r28(Path.cwd())
    folder = Path("phase165_r14_r28_output")
    folder.mkdir(exist_ok=True)
    (folder / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    printable = {key: value for key, value in report.items() if key != "n1_scope_evidence_excerpt"}
    print(json.dumps(printable, ensure_ascii=False, indent=2))
    print("Full context: phase165_r14_r28_output/report.json")


if __name__ == "__main__":
    main()
