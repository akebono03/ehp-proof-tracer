from pathlib import Path
import json
from phase165_r14_r36_adopted_backward import audit_r36


def main():
    report = audit_r36(Path(__file__).with_name("toda_51_complete.tex"))
    out = Path("phase165_r14_r36_output")
    out.mkdir(exist_ok=True)
    (out / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
