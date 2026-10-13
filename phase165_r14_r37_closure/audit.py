import json
from pathlib import Path
from phase165_r14_r37_closure import audit_r37


def main():
    report = audit_r37(Path(__file__).with_name("toda_51_complete.tex"))
    folder = Path("phase165_r14_r37_output")
    folder.mkdir(exist_ok=True)
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in report.items() if k != "leaves"}, ensure_ascii=False, indent=2))
    print("Phase165 closure:", "PASS" if report["phase165_closed"] else "BLOCKED")
    if report["phase165_closed"]:
        Path("phase165_r14_r37_output/phase_closed.flag").write_text("PASS\n", encoding="utf-8")


if __name__ == "__main__":
    main()
