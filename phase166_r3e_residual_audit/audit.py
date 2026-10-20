"""Read-only runtime audit for Phase 166 R3-E residual findings."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import render_partial_proof_markdown
from phase165_r57_r10_step_narrative import has_transport_proof_ancestry, ordered_proof_ancestry
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "audit_result.json"


def inspect_case(n: int, k: int) -> dict:
    result = search_group_from_registered_goal(n=n, k=k)
    markdown = render_partial_proof_markdown(result)
    roots = [step for step in result.proven_steps if step.conclusion == result.conclusion] if result.conclusion is not None else []
    root = roots[0] if len(roots) == 1 else None
    ancestry = ordered_proof_ancestry(root) if root is not None else ()
    names = [str(getattr(step.inference_rule, "name", "") or "") for step in ancestry if step.rule is ProofRule.INFERENCE]
    citations = []
    for step in ancestry:
        if step.rule is ProofRule.GIVEN:
            ref = getattr(step.inference_rule, "literature_reference", None)
            citations.append(str(getattr(ref, "locator", "") or getattr(ref, "label", "") or ""))
    return {
        "n": n, "k": k, "status": result.status.value,
        "open_goals": [repr(g) for g in result.open_goals],
        "diagnostics": list(result.diagnostics),
        "unique_root": root is not None,
        "root_inference_rule": (str(getattr(root.inference_rule, "name", "")) if root else None),
        "ancestor_inference_rule_names": names,
        "given_reference_locators": citations,
        "has_transport_proof_ancestry": has_transport_proof_ancestry(root) if root else False,
        "raw_quotient_rule_in_markdown": "infinite cyclic quotient structure" in markdown,
        "generic_eta_specialization_in_ancestry": "Toda Proposition 5.1 generic higher-eta specialization" in names,
        "narrative": markdown,
    }


def run() -> dict:
    cases = [inspect_case(3, 1), inspect_case(4, 1)]
    return {
        "phase": "166 R3-E residual audit",
        "production_code_modified": False,
        "full_pytest_run": False,
        "cases": cases,
    }


def main() -> None:
    result = run()
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"phase": result["phase"], "cases": [{key: value for key, value in case.items() if key != "narrative"} for case in result["cases"]]}, ensure_ascii=False, indent=2))
    print("Full audit:", OUT)


if __name__ == "__main__":
    main()
