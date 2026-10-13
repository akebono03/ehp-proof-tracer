import json
from pathlib import Path
from phase165_r14_r35_leaf_binding import audit_r35


def main():
    report = audit_r35(Path(__file__).with_name("toda_51_complete.tex"))
    out = Path("phase165_r14_r35_output")
    out.mkdir(exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(json.dumps({k:v for k,v in report.items() if k!="leaf_bindings"}, ensure_ascii=False, indent=2))
    for leaf in report["leaf_bindings"]:
        print(f"{leaf['number']}. {leaf['status']} | {leaf['candidate_locator']} | {leaf['goal']}")


if __name__ == "__main__":
    main()
