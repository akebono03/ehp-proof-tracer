import json
from pathlib import Path
from phase165_r14_r30_hopf_surjective import audit_r30


def main():
    report = audit_r30(Path(__file__).with_name("toda_51_complete.tex"))
    folder = Path("phase165_r14_r30_output")
    folder.mkdir(exist_ok=True)
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
