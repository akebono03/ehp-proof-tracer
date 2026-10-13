import json
from pathlib import Path
from phase165_r14_r34_backward_search import audit_r34


def main():
    report = audit_r34()
    folder = Path("phase165_r14_r34_output")
    folder.mkdir(exist_ok=True)
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8",
    )
    print(json.dumps({k:v for k,v in report.items() if k != "unresolved_leaves"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
