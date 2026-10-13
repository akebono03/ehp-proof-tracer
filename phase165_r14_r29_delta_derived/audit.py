import json
from pathlib import Path
from phase165_r14_r29_delta_derived import audit_r29


def main():
    report = audit_r29(Path(__file__).with_name("toda_51_complete.tex"))
    folder = Path("phase165_r14_r29_output")
    folder.mkdir(exist_ok=True)
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
