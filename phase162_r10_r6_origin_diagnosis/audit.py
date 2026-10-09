"""Phase 162 R10-R6: read-only, evidence-scoped line-to-ProofStep diagnosis.

The R10-R5 JSON is the source of truth. This module never imports the
project or modifies its source. A candidate is evidence, not a proof that
a displayed sentence was logically derived from that step.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict, deque
from pathlib import Path


INPUT_NAME = "phase162_r10_r5_prose_origin.json"
REPORT_NAME = "phase162_r10_r6_origin_diagnosis.md"
JSON_NAME = "phase162_r10_r6_origin_diagnosis.json"


def normalize(value: str) -> str:
    result = re.sub(r"\s+", "", value or "")
    for token in (r"\left", r"\right", r"\,", r"\;", r"\!", r"\quad", r"\qquad"):
        result = result.replace(token, "")
    return result


def risk_tags(row: dict) -> list[str]:
    text = normalize(row.get("text", ""))
    math = normalize(" ".join(row.get("math", [])))
    tags = []
    if ("\\pi_{3}^{2}" in text or "\\pi_3^2" in text) and ("\\pi_{3}^{3}" in text or "\\pi_3^3" in text) and ("H:" in text or "H:" in math):
        tags.append("OFF_TARGET_H_MAP")
    if "\\Delta\\left(\\iota_{5}\\right)" in text or "\\Delta(\\iota_{5})" in text or "\\Delta(\\iota_5)" in text:
        tags.append("DELTA_IOTA5")
    if "[\\iota_{2},\\iota_{2}]" in text or "[\\iota_2,\\iota_2]" in text:
        tags.append("WHITEHEAD_SQUARE")
    if "証明木に記録された群構造の移送" in row.get("text", "") or row.get("origin") == "TRANSPORT_APPENDIX":
        tags.append("TRANSPORT_APPENDIX")
    if row.get("origin") == "MATH_WITHOUT_EXACT_STEP":
        tags.append("NO_EXACT_LATEX_MATCH")
    return tags


def find_roots(steps: dict[int, dict]) -> list[int]:
    return sorted(index for index, node in steps.items() if not node.get("parent_node_ids"))


def parent_path(start: int, steps: dict[int, dict], roots: list[int]) -> list[int] | None:
    if start not in steps:
        return None
    frontier = deque([(start, [start])])
    visited = {start}
    while frontier:
        current, chain = frontier.popleft()
        if current in roots:
            return chain
        for parent in steps[current].get("parent_node_ids", []):
            if parent in steps and parent not in visited:
                visited.add(parent)
                frontier.append((parent, chain + [parent]))
    return None


def structural_candidate_ids(row: dict, steps: dict[int, dict]) -> dict[str, list[int]]:
    """Return strict and weaker evidence separately; never assert semantic equivalence."""
    direct = sorted(set(i for i in row.get("candidate_step_ids", []) if i in steps))
    line_math = [normalize(x) for x in row.get("math", []) if normalize(x)]
    line_text = normalize(row.get("text", ""))
    substring = []
    for i, step in steps.items():
        expr = normalize(step.get("statement_latex") or "")
        if not expr or i in direct or len(expr) < 12:
            continue
        if any(expr in m or m in expr for m in line_math if len(m) >= 12):
            substring.append(i)
        elif expr in line_text:
            substring.append(i)
    return {"exact": direct, "partial_latex": sorted(substring)}


def analyze(data: dict) -> dict:
    steps = {item["id"]: item for item in data["steps"]}
    roots = find_roots(steps)
    rows = data["body_lines"]
    by_text: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        normalized_text = normalize(row.get("text", ""))
        if normalized_text:
            by_text[normalized_text].append(row["line"])
    duplicate_steps: dict[str, list[int]] = defaultdict(list)
    for item in steps.values():
        math = normalize(item.get("statement_latex") or "")
        if math:
            duplicate_steps[math].append(item["id"])
    results = []
    for row in rows:
        candidates = structural_candidate_ids(row, steps)
        exact_path = {str(i): parent_path(i, steps, roots) for i in candidates["exact"]}
        partial_path = {str(i): parent_path(i, steps, roots) for i in candidates["partial_latex"]}
        repeated_lines = by_text[normalize(row.get("text", ""))]
        match_exprs = [normalize(steps[i].get("statement_latex") or "") for i in candidates["exact"]]
        same_statement_nodes = sorted({j for expr in match_exprs for j in duplicate_steps.get(expr, [])})
        tags = risk_tags(row)
        results.append({
            "line": row["line"], "text": row.get("text", ""),
            "original_origin": row.get("origin"), "tags": tags,
            "exact_step_ids": candidates["exact"],
            "partial_latex_step_ids": candidates["partial_latex"],
            "exact_paths_node_to_root": exact_path,
            "partial_paths_node_to_root": partial_path,
            "duplicate_text_lines": repeated_lines if len(repeated_lines) > 1 else [],
            "same_statement_node_ids": same_statement_nodes if len(same_statement_nodes) > 1 else [],
            "diagnosis": (
                "DIRECT_STEP_CANDIDATE" if candidates["exact"] else
                "PARTIAL_EXPRESSION_ONLY" if candidates["partial_latex"] else
                "NO_STEP_TEXT_MATCH"
            ),
        })
    tags_summary = Counter(tag for row in results for tag in row["tags"])
    group_summary = Counter(row["diagnosis"] for row in results)
    appendix = data.get("transport_paragraph")
    root_latex = [steps[i].get("statement_latex") for i in roots]
    appendix_note = (
        "祖先中の移送経路由来。最終目標そのものへの移送かは未認証。"
        if appendix else "末尾の独立追加段落なし。"
    )
    return {
        "source_file": INPUT_NAME, "source_summary": data.get("summary", {}),
        "root_step_ids": roots, "root_latex": root_latex,
        "summary": {"body_rows": len(results), "diagnoses": dict(group_summary), "tags": dict(tags_summary),
                    "duplicate_text_groups": sum(1 for v in by_text.values() if len(v) > 1),
                    "duplicate_math_node_groups": sum(1 for v in duplicate_steps.values() if len(v) > 1)},
        "rows": results,
        "transport": {"paragraph": appendix, "diagnosis": appendix_note},
        "warnings": [
            "同じ数学式の候補が複数ある場合、どれが実際に Renderer に採用されたかはこの JSON のみでは確定できない。",
            "一致しない数式については、説明文中の合成式・数式フォーマットの違いも考えられる。",
            "証明木から最終結論に到達する依存経路は、数学的必要性や前提の妥当性を証明しない。",
        ],
    }


def write_reports(report: dict, folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / JSON_NAME).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Phase 162 R10-R6：本文と証明木の個別原因監査", "", "## 集計", ""]
    lines += [f"- {key}: {value}" for key, value in report["summary"].items()]
    lines += ["", "## 優先調査項目", ""]
    for label in ("OFF_TARGET_H_MAP", "DELTA_IOTA5", "WHITEHEAD_SQUARE", "TRANSPORT_APPENDIX"):
        subset = [r for r in report["rows"] if label in r["tags"]]
        lines += [f"### {label}：{len(subset)} 行", ""]
        for r in subset:
            lines.append(f"- 本文行 {r['line']}：{r['text']}")
            lines.append(f"  - 数式完全一致ノード：{r['exact_step_ids']}")
            lines.append(f"  - 部分一致候補：{r['partial_latex_step_ids']}")
            lines.append(f"  - 最終結論への経路：{r['exact_paths_node_to_root'] or r['partial_paths_node_to_root']}")
            lines.append(f"  - 同文の重複行：{r['duplicate_text_lines']}")
            lines.append(f"  - 同数式の重複ノード：{r['same_statement_node_ids']}")
        lines.append("")
    lines += ["## 数式完全一致がない項目", ""]
    for r in report["rows"]:
        if r["original_origin"] == "MATH_WITHOUT_EXACT_STEP":
            lines.append(f"- 行 {r['line']}：{r['text']}")
            lines.append(f"  - 部分一致候補：{r['partial_latex_step_ids']}、診断：{r['diagnosis']}")
    lines += ["", "## 全本文項目", "", "| 行 | 原分類 | 判定 | 一致ノード | 部分候補 | 重複行 | 本文 |", "|---:|---|---|---|---|---|---|"]
    for r in report["rows"]:
        value = r["text"].replace("|", "\\|").replace("`", "'")[:140]
        lines.append(f"| {r['line']} | {r['original_origin']} | {r['diagnosis']} | {r['exact_step_ids']} | {r['partial_latex_step_ids']} | {r['duplicate_text_lines']} | {value} |")
    lines += ["", "## stable 移送段落", "", report["transport"]["diagnosis"], "", report["transport"]["paragraph"] or "なし", "", "## 解釈上の注意", ""]
    lines += [f"- {warning}" for warning in report["warnings"]]
    (folder / REPORT_NAME).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path.cwd() / INPUT_NAME)
    parser.add_argument("--out", type=Path, default=Path.cwd())
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8-sig"))
    for field in ("steps", "body_lines", "summary"):
        if field not in data:
            raise ValueError(f"R10-R5 audit input missing: {field}")
    report = analyze(data)
    write_reports(report, args.out)
    print("Phase 162 R10-R6 read-only origin diagnosis")
    print("Nodes:", report["source_summary"].get("nodes"))
    print("Body rows:", report["summary"]["body_rows"])
    print("Classified:", report["summary"]["diagnoses"])
    print("Targeted rows:", report["summary"]["tags"])
    print("Markdown:", args.out / REPORT_NAME)
    print("JSON:", args.out / JSON_NAME)


if __name__ == "__main__":
    main()
