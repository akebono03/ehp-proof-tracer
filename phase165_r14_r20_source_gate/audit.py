import json
from pathlib import Path
from phase165_r14_r20_source_gate import audit_r20


def main():
    report = audit_r20()
    out = Path("phase165_r14_r20_output")
    out.mkdir(exist_ok=True)
    (out / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "report.md").write_text(
        "# Phase 165 R14-R20\n\n"
        + "\n".join(f"- {k}: {v}" for k, v in report.items() if k != "prop42_candidates")
        + "\n\n## Proposition 4.2 候補\n\n"
        + "\n\n".join(f"### {r['assertion_id']}\n\n```tex\n{r['source_text']}\n```"
                     for r in report["prop42_candidates"]) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "prop42_candidates"}
                     | {"prop42_candidate_count": len(report["prop42_candidates"])},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
