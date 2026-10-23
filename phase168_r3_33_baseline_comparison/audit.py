"""R3-33: compare model-backed narrative with the frozen Phase 168 baselines.

Audit only. Each expected mathematical milestone is independently specified,
not recovered from the current renderer output. No normalization changes proof.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))
OUTPUT = PACKAGE / "output"


def normalize(text: str) -> str:
    """Normalize only benign TeX whitespace and common math delimiters."""
    return re.sub(r"\s+", "", text.replace("$", "").replace(r"\left", "").replace(r"\right", ""))


CASES = (
    {
        "name": "pi_3^2", "n": 2, "k": 1, "baseline": "pi3_2_original.txt",
        "milestones": (
            ("complete_ehp_sequence", r"\pi_{2}^{1}\xrightarrow{E}\pi_{3}^{2}\xrightarrow{H}\pi_{3}^{3}\xrightarrow{\Delta}\pi_{1}^{1}\xrightarrow{E}\pi_{2}^{2}"),
            ("pi21_zero", r"\pi_{2}^{1}=0"),
            ("hopf_injective", "は単射"),
            ("pi11_free", r"\pi_{1}^{1}=\mathbb{Z}\{\iota_{1}\}"),
            ("pi22_free", r"\pi_{2}^{2}=\mathbb{Z}\{\iota_{2}\}"),
            ("suspension_generator", r"E(\iota_{1})=\iota_{2}"),
            ("suspension_iso", "は同型"),
            ("delta_zero", "は零写像"),
            ("hopf_surjective", "は全射"),
            ("hopf_iso", "は同型"),
            ("pi33_free", r"\pi_{3}^{3}=\mathbb{Z}\{\iota_{3}\}"),
            ("hopf_generator", r"H(\eta_{2})=\iota_{3}"),
            ("final_group", r"\pi_{3}^{2}=\mathbb{Z}\{\eta_{2}\}"),
        ),
    },
    {
        "name": "pi_4^3", "n": 3, "k": 1, "baseline": "pi4_3_original.txt",
        "milestones": (
            ("complete_ehp_sequence", r"\pi_{5}^{5}\xrightarrow{\Delta}\pi_{3}^{2}\xrightarrow{E}\pi_{4}^{3}\xrightarrow{H}\pi_{4}^{5}"),
            ("suspension_generator", r"E(\eta_{2})=\eta_{3}"),
            ("diagonal_general", r"\pi_{n}^{n}=\mathbb{Z}\{\iota_{n}\}"),
            ("pi55_free", r"\pi_{5}^{5}=\mathbb{Z}\{\iota_{5}\}"),
            ("delta_generator", r"\Delta(\iota_{5})=\pm2\eta_{2}"),
            ("delta_image", r"\operatorname{Im}\Delta=\mathbb{Z}\{2\eta_{2}\}"),
            ("kernel", r"\kerE=\mathbb{Z}\{2\eta_{2}\}"),
            ("pi45_zero", r"\pi_{4}^{5}=0"),
            ("suspension_surjective", "は全射"),
            ("source_group", r"\pi_{3}^{2}=\mathbb{Z}\{\eta_{2}\}"),
            ("quotient", r"\pi_{4}^{3}\cong\pi_{3}^{2}/\mathbb{Z}\{2\eta_{2}\}"),
            ("final_group", r"\pi_{4}^{3}=\mathbb{Z}/2\{\eta_{3}\}"),
        ),
    },
    {
        "name": "pi_5^4", "n": 4, "k": 1, "baseline": "pi5_4_original.txt",
        "milestones": (
            ("source_group", r"\pi_{4}^{3}=\mathbb{Z}/2\{\eta_{3}\}"),
            ("toda45_specialization", "(n,m,k)=(3,4,1)"),
            ("transport_map", r"E:\pi_{4}^{3}\to\pi_{5}^{4}"),
            ("transport_isomorphism", "は同型"),
            ("generator_transport", r"E\eta_{3}=\eta_{4}"),
            ("final_group", r"\pi_{5}^{4}=\mathbb{Z}/2\{\eta_{4}\}"),
        ),
    },
)


def analyze_markdown(markdown: str, case: dict) -> dict:
    flat = normalize(markdown)
    observations = []
    cursor = -1
    for name, pattern in case["milestones"]:
        at = flat.find(normalize(pattern), cursor + 1)
        anywhere = flat.find(normalize(pattern))
        if at >= 0:
            status = "IN_ORDER"
            cursor = at
        elif anywhere >= 0:
            status = "OUT_OF_ORDER_OR_DUPLICATE"
        else:
            status = "MISSING_OR_DIFFERENT_EXPRESSION"
        observations.append({"milestone": name, "pattern": pattern,
                             "status": status, "first_position": anywhere})
    # Reference numbering is not compared with the historical baseline.
    source = markdown.split("証明\n", 1)[0]
    refs = re.findall(r"^\*\*\[R(\d+)\] (.*?)\.\*\*\s*$", source, re.M)
    return {
        "milestones": observations,
        "in_order_count": sum(x["status"] == "IN_ORDER" for x in observations),
        "missing_or_different_count": sum(x["status"] == "MISSING_OR_DIFFERENT_EXPRESSION" for x in observations),
        "out_of_order_count": sum(x["status"] == "OUT_OF_ORDER_OR_DUPLICATE" for x in observations),
        "reference_headings": refs,
        "complete_sequence_occurrences": markdown.count("次の完全列を考える"),
        "note": "MISSING_OR_DIFFERENT_EXPRESSION is a literal comparison, not a mathematical invalidity verdict",
    }


def runtime_case(case: dict) -> dict:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown

    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=case["n"], k=case["k"], bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    markdown = render_model_backed_narrative_markdown(result, model)
    comparison = analyze_markdown(markdown, case)
    actual_refs = [(int(a), b) for a, b in comparison["reference_headings"]]
    model_refs = [(c.number, c.reference.locator or c.reference.label) for c in model.citations]
    comparison.update({
        "status": str(result.status), "step_count": len(model.steps),
        "model_reference_matches": actual_refs == model_refs,
        "baseline_file": case["baseline"],
        "baseline_text": (PACKAGE / "baselines" / case["baseline"]).read_text(encoding="utf-8"),
    })
    (OUTPUT / f"{case['name']}_current.txt").write_text(markdown, encoding="utf-8")
    return comparison


def main():
    OUTPUT.mkdir(exist_ok=True)
    results = {}
    for case in CASES:
        try:
            results[case["name"]] = runtime_case(case)
        except Exception as exc:
            results[case["name"]] = {"error": f"{type(exc).__name__}: {exc}"}
    document = {"phase": "168 R3-33", "status": "AUDIT_ONLY", "results": results,
                "limitations": [
                    "Expression checks are conservative literal tokens, not semantic theorem equivalence.",
                    "Out-of-order status may reflect repeated phrases such as 'は同型'.",
                    "Reference numbers from the historical baseline are intentionally ignored.",
                    "Frozen baseline files are preserved byte-for-byte.",
                    "No production code is modified and full pytest is not run."]}
    (OUTPUT / "baseline_comparison.json").write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 168 R3-33 — 固定基準比較", "", "判定: AUDIT_ONLY", "",
             "| 群 | 順序一致 | 欠落・表記差 | 順序差・重複 | Reference一致 |",
             "|---|---:|---:|---:|---|"]
    for name, r in results.items():
        lines.append(f"| {name} | {r.get('in_order_count','-')} | "
                     f"{r.get('missing_or_different_count','-')} | "
                     f"{r.get('out_of_order_count','-')} | "
                     f"{r.get('model_reference_matches','ERROR')} |")
        lines.extend(["", f"## {name}", ""])
        if "error" in r:
            lines.append(r["error"])
        else:
            for item in r["milestones"]:
                lines.append(f"- {item['milestone']}: {item['status']}")
    lines.extend(["", "## 注意", ""] + [f"- {x}" for x in document["limitations"]])
    report = "\n".join(lines) + "\n"
    (OUTPUT / "baseline_comparison.md").write_text(report, encoding="utf-8")
    print(report)
    print("REPORT:", OUTPUT / "baseline_comparison.json")
    return 1 if any("error" in r for r in results.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
