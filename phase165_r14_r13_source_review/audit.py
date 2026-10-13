import json
from pathlib import Path
from phase165_r14_r13_source_review import audit_r13


def main():
    report = audit_r13()
    output = Path("phase165_r14_r13_output")
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "report.md").write_text(
        "# Phase 165 R14-R13 監査\n\n"
        + "## Proposition 4.2 の出典候補\n\n"
        + "\n".join(
            "### " + x["assertion_id"] + "\n\n```tex\n"
            + x["source_text"] + "\n```\n"
            for x in report["source_reviews"]
        )
        + "\n## 対角懸垂の必要条件\n\n"
        + "\n".join("- " + x for x in report["diagonal_suspension"]["requirements"])
        + "\n\n証明認証・ProofStep 生成は行っていません。\n", encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in report.items() if k != "source_reviews"}, ensure_ascii=False, indent=2))
    print("Source texts saved to phase165_r14_r13_output/report.md")


if __name__ == "__main__":
    main()
