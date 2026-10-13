import json
from pathlib import Path

from phase165_r14_r16_foundational_suspension import audit_r16


def main():
    report = audit_r16()
    output = Path("phase165_r14_r16_output")
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    (output / "report.md").write_text(
        "# Phase 165 R14-R16 監査結果\n\n"
        + "\n".join(f"- {k}: {v}" for k,v in report.items()
                    if k != "prop42_candidates")
        + "\n\n## Proposition 4.2 候補（原文）\n\n"
        + "\n\n".join(
            f"### {r['assertion_id']}\n\n```tex\n{r['source_text']}\n```"
            for r in report["prop42_candidates"]
        ) + "\n",
        encoding="utf8")
    summary = {k:v for k,v in report.items() if k != "prop42_candidates"}
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
