from __future__ import annotations

import ast
import json
from pathlib import Path
from web_group_proof import build_standard_web_group_proof_view

TARGETS = ((2, 1), (3, 1))
OUT = Path("phase167_r4_6_specialization_route_results")
MODULES = (
    "toda_group_proof_narrative_renderer.py",
    "toda_group_proof_narrative_contribution_renderer.py",
)
FUNCTIONS = (
    "_phase159_r1_6d_toda_51_diagonal_specialization_lines",
    "_phase159_r1_6d_finalize_reference_and_linkage",
    "order_toda_group_proof_narrative_visible_step_dependencies",
    "order_toda_group_proof_narrative_visible_relation_dependencies",
    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
)


def inspect_sources():
    found = {}
    for name in MODULES:
        source = Path(name).read_text(encoding="utf-8")
        tree = ast.parse(source)
        spans = {}
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in FUNCTIONS:
                spans[node.name] = {
                    "start_line": node.lineno,
                    "end_line": node.end_lineno,
                    "has_reference_51": "(5.1)" in ast.get_source_segment(source, node),
                }
        found[name] = spans
    return found


def capture_group(n, k):
    view = build_standard_web_group_proof_view(n, k, max_depth=2, mode="narrative")
    lines = []
    for index, line in enumerate(view.rendered_lines, start=1):
        lines.append({
            "index": index,
            "kind": line.kind,
            "prefix": line.prefix,
            "statement_latex": line.statement_latex,
            "suffix": line.suffix,
            "segments": [{"kind": s.kind, "value": s.value} for s in line.segments],
        })
    return {"n": n, "k": k, "key": view.key, "lines": lines}


def focus_lines(group):
    return [
        line for line in group["lines"]
        if any(
            marker in " ".join([
                line["prefix"], line["statement_latex"] or "", line["suffix"]
            ])
            for marker in (r"\pi_{n}^{n}", r"\pi_{5}^{5}", r"\pi_{1}^{1}",
                           r"\pi_{2}^{2}", r"\pi_{3}^{3}", "[R1]", "これより")
        )
    ]


def main():
    OUT.mkdir(exist_ok=True)
    results = []
    for n, k in TARGETS:
        group = capture_group(n, k)
        results.append({
            "target": f"pi{n+k}_{n}",
            "key": group["key"],
            "focus_lines": focus_lines(group),
            "count": len(group["lines"]),
        })
        (OUT / f"pi{n+k}_{n}_all_lines.json").write_text(
            json.dumps(group, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"CAPTURED: pi{n+k}_{n}: {len(group['lines'])} lines")
    report = {"source_functions": inspect_sources(), "group_comparison": results}
    (OUT / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("REPORT:", (OUT / "report.json").resolve())
    print("NO_PRODUCTION_CHANGES")


if __name__ == "__main__":
    main()
