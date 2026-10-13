import json
from pathlib import Path
from phase165_r14_r14_diagonal_and_prop42 import audit_r14

def main():
    result = audit_r14()
    out = Path("phase165_r14_r14_output")
    out.mkdir(exist_ok=True)
    (out / "report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf8")
    sections = ["# Phase 165 R14-R14 出典照合", "## Proposition 4.2 candidates"]
    for row in result["prop42_source_candidates"]:
        sections.extend((f"### {row['assertion_id']}", "```tex", row["source_text"], "```"))
    sections.extend(("## 対角懸垂の未解決前提", *("- "+g for g in result["diagonal_subgoals"])))
    (out / "report.md").write_text("\n\n".join(sections)+"\n", encoding="utf8")
    summary = {key: val for key,val in result.items() if key != "prop42_source_candidates"}
    summary["prop42_candidate_count"] = len(result["prop42_source_candidates"])
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
