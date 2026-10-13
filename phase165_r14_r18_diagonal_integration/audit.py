import json
from pathlib import Path
from phase165_r14_r18_diagonal_integration import audit_r18


def main():
    report = audit_r18()
    target = Path("phase165_r14_r18_output")
    target.mkdir(exist_ok=True)
    (target / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (target / "report.md").write_text(
        "# Phase 165 R14-R18 — 実装・出典監査\n\n"
        + "\n".join(f"- {k}: {v}" for k, v in report.items() if k != "prop42_source_texts")
        + "\n\n## Proposition 4.2 候補原文\n\n"
        + "\n\n".join(f"### {x['assertion_id']}\n\n```tex\n{x['source_text']}\n```" for x in report["prop42_source_texts"])
        + "\n", encoding="utf-8"
    )
    shown = {k: v for k,v in report.items() if k != "prop42_source_texts"}
    print(json.dumps(shown, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
