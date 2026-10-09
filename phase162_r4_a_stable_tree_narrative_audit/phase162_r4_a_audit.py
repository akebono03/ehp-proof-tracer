"""Read-only Phase 162 R4-A audit. Run from the repository root."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tests.test_phase143_19_method_evidence import _method_evidence_data
import toda_group_proof_narrative_renderer as renderer


FEATURES = {
    "toda45": ("Toda45IsomorphismStatement", "(4.5)"),
    "base_group": ("Relation", "Proposition 5.1"),
    "generator_transport": ("IteratedSuspension", "E\\eta_{3}"),
    "target_structure": ("Relation", r"\pi_{5}^{4}"),
}


def collect_steps(root):
    """Traverse actual ProofStep.premises by object identity, with cycle guard."""
    found = []
    seen = set()

    def visit(step, depth):
        if id(step) in seen:
            return
        seen.add(id(step))
        rule = getattr(step, "inference_rule", None)
        reference = getattr(rule, "literature_reference", None) if rule is not None else None
        found.append({
            "index": len(found),
            "depth": depth,
            "type": type(step.conclusion).__name__,
            "conclusion_repr": repr(step.conclusion),
            "proof_rule": str(getattr(step, "rule", None)),
            "inference_rule": getattr(rule, "name", None),
            "literature_reference": repr(reference) if reference is not None else None,
            "premise_count": len(step.premises),
            "object_id": id(step),
        })
        for premise in step.premises:
            visit(premise, depth + 1)

    visit(root, 0)
    return found


def reference_locator(ref):
    if ref is None:
        return None
    return getattr(ref, "locator", None) or getattr(ref, "label", None) or repr(ref)


def audit():
    presentation, _, _, _ = _method_evidence_data(4, 1)
    public = renderer.render_toda_group_proof_narrative_markdown(presentation)
    baseline_error = None
    try:
        baseline = renderer._phase158_baseline_render_toda_group_proof_narrative_markdown(presentation)
    except Exception as exc:
        baseline = ""
        baseline_error = f"{type(exc).__name__}: {exc}"
    root_steps = collect_steps(presentation.root_step)
    nodes = [node.proof_step for node in presentation.nodes]
    node_ids = {id(step) for step in nodes}
    edges = [
        {"parent_type": type(edge.parent_step.conclusion).__name__,
         "premise_type": type(edge.premise_step.conclusion).__name__,
         "premise_index": edge.premise_index}
        for edge in presentation.edges
    ]
    checks = {}
    for key, (type_name, marker) in FEATURES.items():
        matching_tree = [step["index"] for step in root_steps if step["type"] == type_name]
        matching_presentation = [i for i, step in enumerate(nodes) if type(step.conclusion).__name__ == type_name]
        public_has = marker in public
        baseline_has = marker in baseline
        # A type match is only an indication, not a logical derivation proof.
        if matching_tree:
            status = "TREE_PRESENT_CANDIDATE"
        elif matching_presentation:
            status = "PRESENTATION_ONLY_CANDIDATE"
        elif public_has or baseline_has:
            status = "RENDERER_ONLY_CANDIDATE"
        else:
            status = "MISSING"
        checks[key] = {
            "status": status,
            "tree_step_indices": matching_tree,
            "presentation_node_indices": matching_presentation,
            "public_contains_marker": public_has,
            "baseline_contains_marker": baseline_has,
            "marker": marker,
            "note": "Type and text markers are diagnostic only; inspect conclusion_repr and edges to establish mathematical dependency.",
        }
    return {
        "scope": "pi_5^4; observational audit; no production mutation",
        "root_conclusion": repr(presentation.root_step.conclusion),
        "tree_steps": root_steps,
        "presentation_node_count": len(nodes),
        "presentation_edge_count": len(edges),
        "root_nodes_in_presentation": sum(id(step) == id(presentation.root_step) for step in nodes),
        "tree_steps_visible_in_presentation": sum(step["object_id"] in node_ids for step in root_steps),
        "presentation_edges": edges,
        "checks": checks,
        "render_paths": {
            "public": "render_toda_group_proof_narrative_markdown",
            "baseline": "_phase158_baseline_render_toda_group_proof_narrative_markdown",
            "baseline_caveat": "Baseline performs semantic closure and is not a raw ProofStep-only renderer.",
        },
        "public_markdown": public,
        "baseline_markdown": baseline,
        "baseline_error": baseline_error,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="phase162_r4_a_stable_tree_narrative_audit/audit_output")
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    report = audit()
    (out / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "public.md").write_text(report["public_markdown"], encoding="utf-8")
    (out / "baseline.md").write_text(report["baseline_markdown"], encoding="utf-8")
    lines = ["# Phase 162 R4-A 監査結果", "", "対象: $\\pi_5^4$", "", "## 判定（候補分類であり、数学的な証明認定ではない）", ""]
    for key, item in report["checks"].items():
        lines.append(f"- {key}: {item['status']} / tree={item['tree_step_indices']} / presentation={item['presentation_node_indices']} / public={item['public_contains_marker']} / baseline={item['baseline_contains_marker']}")
    lines += ["", "## 証明木", "", f"root: `{report['root_conclusion']}`", "", "| index | depth | statement type | inference rule | reference | premises |", "|---:|---:|---|---|---|---:|"]
    for step in report["tree_steps"]:
        lines.append(f"| {step['index']} | {step['depth']} | {step['type']} | {step['inference_rule']} | {step['literature_reference']} | {step['premise_count']} |")
    lines += ["", "## baseline経路の例外", "", report["baseline_error"] or "なし", "", "## 解釈上の注意", "", "- type 名の出現だけでは、結論に必要な数学的依存関係の存在を証明しない。", "- `public.md` は現在のstable専用経路を含む。", "- `baseline.md` は既存baselineを呼び出すが、semantic closureを含む。", "- `audit.json` の各 conclusion_repr と presentation_edges を照合してR4-Bの方針を判断する。", "- R4-Aでは削除・公開関数の切替・推論規則の追加を行わない。", ""]
    (out / "comparison.md").write_text("\n".join(lines), encoding="utf-8")
    print("Audit files:", *(str(out / name) for name in ("comparison.md", "audit.json", "public.md", "baseline.md")), sep="\n  ")
    for key, check in report["checks"].items():
        print(f"{key}: {check['status']}")


if __name__ == "__main__":
    main()
