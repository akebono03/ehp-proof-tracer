"""Report the actual source result and ongoing gaps without implying proof closure."""
from __future__ import annotations

import json
from pathlib import Path

from phase169_r3m_prior_result_catalog.audit import build_report


def main():
    from web_group_proof import build_standard_web_group_proof_view
    report = build_report()
    # Distinguish observed exploration from the real root's ancestry.
    from phase169_r3j1_narrative_import_isolation.audit import capture_actual_narrative
    result, model, markdown, pi53_view = capture_actual_narrative()
    root = model.steps[model.root_index]
    ancestral_ids = set()
    def visit(step):
        if id(step) in ancestral_ids:
            return
        ancestral_ids.add(id(step))
        for parent in step.premises:
            visit(parent)
    visit(root)
    ancestral_indices = tuple(i for i, step in enumerate(model.steps)
                             if id(step) in ancestral_ids)
    number_by_locator = {
        citation.reference.locator: citation.number
        for citation in model.citations
    }
    def linked_to_ancestor(locator):
        number = number_by_locator.get(locator)
        return None if number is None else any(
            number in model.step_citation_numbers[i] for i in ancestral_indices
        )
    report["pi5_3_ancestry"] = {
        "observed_steps": len(model.steps),
        "root_ancestry_steps": len(ancestral_indices),
        "toda52_in_root_ancestry": linked_to_ancestor("(5.2)"),
        "prop53_in_root_ancestry": linked_to_ancestor("Proposition 5.3"),
    }
    print("R3N_PI53_TODA52_IN_ROOT_ANCESTRY="
          + str(report["pi5_3_ancestry"]["toda52_in_root_ancestry"]))
    print("R3N_PI53_PROP53_IN_ROOT_ANCESTRY="
          + str(report["pi5_3_ancestry"]["prop53_in_root_ancestry"]))
    cases = []
    for n, k in ((3, 2), (4, 2), (5, 2), (6, 2)):
        view = build_standard_web_group_proof_view(n=n, k=k, mode="narrative", citation_source="model")
        cases.append({
            "n": n, "k": k,
            "web_key": view.key,
            "partial": view.partial_result,
            "display_status": "partial" if view.partial_result else "complete",
        })
        print(f"R3N_WEB_PI_{n+k}_{n}=" + cases[-1]["display_status"])
    report.update({
        "phase": "169-R3N",
        "search_alias_connection": True,
        "previous_proof_completion_required": False,
        "only_prior_fixed_sources_accepted": True,
        "web_cases": cases,
        "note": "Stable 2-stem transport/eta-square normalization is not implemented by this patch.",
    })
    output = Path(__file__).resolve().parent / "output" / "r3n_report.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("R3N_REPORT=" + str(output))
    print("R3N_PRIOR_PROOF_COMPLETION_REQUIRED=False")
    print("R3N_AUDIT_COMPLETE=True")


if __name__ == "__main__":
    main()
