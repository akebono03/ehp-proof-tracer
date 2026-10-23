"""Read-only audit of linked citation assertions and their reference-body renderability."""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))
OUTPUT = Path(__file__).resolve().parent / "output"
CASES = ((2, 1), (3, 1), (4, 1))


def inspect_case(n: int, k: int) -> dict:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from web_group_proof_common import _group_proof_statement_latex

    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    registry = getattr(bridge, "registry", None)
    if registry is None:
        registry = getattr(bridge, "statement_registry", None)
    citations = []
    for citation in model.citations:
        attached = []
        for assertion_id in citation.assertion_ids:
            info = {"id": assertion_id}
            if registry is None:
                info["registry_lookup"] = "REGISTRY_NOT_AVAILABLE_ON_BRIDGE"
            else:
                try:
                    assertion = registry.assertion(assertion_id)
                    content = assertion.content
                    latex, fallback = _group_proof_statement_latex(content)
                    info.update({
                        "reference_id": assertion.reference_id,
                        "content_type": type(content).__name__,
                        "content_repr": repr(content)[:1200],
                        "latex": latex,
                        "fallback_type": fallback,
                        "renderable": bool(latex is not None and fallback is None),
                    })
                except Exception as exc:
                    info["registry_lookup_error"] = f"{type(exc).__name__}: {exc}"
            attached.append(info)
        step_facts = []
        for idx in citation.step_indices:
            step = model.steps[idx]
            latex, fallback = _group_proof_statement_latex(step.conclusion)
            step_facts.append({
                "step_index": idx,
                "conclusion_type": type(step.conclusion).__name__,
                "conclusion_repr": repr(step.conclusion)[:900],
                "latex": latex,
                "fallback_type": fallback,
                "model_step_cites_number": citation.number in model.step_citation_numbers[idx],
            })
        citations.append({
            "number": citation.number,
            "locator": citation.reference.locator or citation.reference.label,
            "assertion_ids": list(citation.assertion_ids),
            "reference_ids": list(citation.reference_ids),
            "step_indices": list(citation.step_indices),
            "assertions": attached,
            "cited_steps": step_facts,
        })
    return {
        "group": f"pi_{n+k}^{n}", "search_status": str(result.status),
        "step_count": len(model.steps), "reference_count": len(citations),
        "registry_available": registry is not None,
        "citations": citations,
    }


def main() -> int:
    result = {"phase": "168 R3-35", "status": "AUDIT_ONLY", "cases": [],
              "note": "No content is constructed from a literature locator; all candidates are model-linked assertions or proof steps."}
    for n, k in CASES:
        try:
            result["cases"].append(inspect_case(n, k))
        except Exception as exc:
            result["cases"].append({"group": f"pi_{n+k}^{n}",
                                    "error": f"{type(exc).__name__}: {exc}"})
    OUTPUT.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT / "reference_content_audit.json"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    report = ["# Phase 168 R3-35 — Reference 命題本文の接続監査", "", "監査専用・変更なし", ""]
    for case in result["cases"]:
        report.extend([f"## {case['group']}", ""])
        if "error" in case:
            report.append("ERROR: " + case["error"])
            continue
        report.append(f"registry_available: {case['registry_available']}")
        for citation in case["citations"]:
            report.extend(["", f"### [R{citation['number']}] {citation['locator']}",
                           f"assertion_ids: {citation['assertion_ids']}",
                           f"reference_ids: {citation['reference_ids']}",
                           f"step_indices: {citation['step_indices']}"])
            for a in citation["assertions"]:
                report.append(f"- assertion {a['id']}: type={a.get('content_type')}, renderable={a.get('renderable')}, latex={a.get('latex')}, problem={a.get('registry_lookup', a.get('registry_lookup_error'))}")
            for step in citation["cited_steps"]:
                report.append(f"- step {step['step_index']}: type={step['conclusion_type']}, latex={step['latex']}, fallback={step['fallback_type']}")
    report.extend(["", "## 判断の限界", "",
                   "- 引用された命題内容と固定基準の一般公式が一致するかは、出力を個別に照合する必要がある。",
                   "- 引用された具体的ステップを一般命題として言い換えることはしない。",
                   "- 監査は source/assertion の型と引用接続を記録するだけで、本文を変更しない。"])
    (OUTPUT / "reference_content_audit.md").write_text("\n".join(report)+"\n", encoding="utf-8")
    print("\n".join(report))
    print("JSON:", json_path)
    return 1 if any("error" in case for case in result["cases"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
