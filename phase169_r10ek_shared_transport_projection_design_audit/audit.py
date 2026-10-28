"""Audit-only study of the existing cyclic and direct-sum transport display paths."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10a_verified_stable_chain_projection.projection import (
    project_verified_stable_image_chain,
)
from phase169_r10ec_direct_sum_narrative_projection.projection import (
    project_verified_direct_sum_transport,
)
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations,
)

from .contract import CASES, AuditCase, inspect_shared_contract


def inspect_case(bridge: object, case: AuditCase, output: Path) -> dict:
    """Compare verified *existing* presentation objects, without altering them."""
    contexts = []
    result = search_group_from_registered_goal(
        n=case.n, k=case.k, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or result.open_goals or len(contexts) != 1:
        raise AssertionError(f"incomplete or unscreened proof for {case.group}")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    inferred, given = verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
        derived_target_without_citing_id=citing is None,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    order = tuple(item.step_index for item in project_narrative_order(model))
    saved_ids = tuple(id(step) for step in model.steps)
    saved_premises = tuple(tuple(id(parent) for parent in step.premises)
                           for step in model.steps)
    saved_citations = model.step_citation_numbers

    cyclic = project_verified_stable_image_chain(model, order)
    direct = project_verified_direct_sum_transport(model, order)
    selected = cyclic if case.category == "finite_cyclic" else direct
    excluded = direct if case.category == "finite_cyclic" else cyclic
    if selected is None or excluded is not None:
        raise AssertionError(f"projection dispatch not exclusive for {case.group}")
    row = inspect_shared_contract(model, order, selected, case)
    markdown = render_model_backed_narrative_markdown(result, model)
    if case.category == "finite_cyclic":
        marker = (
            rf"$E^{{{selected.exponent}}}"
            rf"({selected.source_tex})={selected.target_tex}$"
        )
    else:
        marker = selected.statement
    if markdown.count(marker) != 1:
        raise AssertionError(f"certified compressed formula absent or duplicated: {case.group}")
    if any(
        f"**[R{citation.number}] {citation.reference.locator or citation.reference.label}.**"
        not in markdown for citation in model.citations
    ):
        raise AssertionError(f"Reference section lost citations for {case.group}")
    duplicate_count = count_rendered_image_equations(markdown)["extra_duplicate_occurrences"]
    if duplicate_count:
        raise AssertionError(f"one-step generator image duplicated for {case.group}")
    if (saved_ids != tuple(id(step) for step in model.steps)
            or saved_premises != tuple(tuple(id(parent) for parent in step.premises)
                                      for step in model.steps)
            or saved_citations != model.step_citation_numbers
            or len(model.steps) != len(result.proven_steps)
            or not markdown.rstrip().endswith("□")):
        raise AssertionError(f"proof tree changed or completed narrative damaged: {case.group}")
    filename = f"pi_{case.n + case.k}_{case.n}.md"
    (output / filename).write_text(markdown, encoding="utf-8")
    row.update({
        "status": result.status.value,
        "trust": "PASS",
        "verified_inference_steps": inferred,
        "verified_given_steps": given,
        "proof_step_count": len(model.steps),
        "reference_count": len(model.citations),
        "one_step_equations": count_rendered_image_equations(markdown)["total_occurrences"],
        "duplicate_equations": duplicate_count,
        "proof_tree_preserved": True,
        "reference_preserved": True,
        "rendered_file": filename,
    })
    return row


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        raise SystemExit("Usage: python -m phase169_r10ek_shared_transport_projection_design_audit.audit OUTPUT_DIRECTORY")
    output = Path(args[0]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    bridge = build_shared_typed_bridge()
    rows = [inspect_case(bridge, case, output) for case in CASES]
    report = {
        "phase": "169 R10EK",
        "mode": "AUDIT_ONLY",
        "unification_implemented": False,
        "shared_contract_tested": True,
        "current_cyclic_and_direct_sum_implementations_retained": True,
        "not_covered": [
            "free cyclic proof presentation",
            "zero groups",
            "one-stem eta-notation special route",
            "incomplete 11-stem and 14-stem cases",
            "all possible stem and generator structures",
        ],
        "design_recommendation": (
            "Extract only common verified ancestry/citation/external-consumer checks "
            "after a separate equivalence and safety audit; keep group-specific "
            "endpoint notation and no-proof-evidence boundary."
        ),
        "cases": rows,
        "full_pytest_run": False,
        "production_files_changed": False,
    }
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    for row in rows:
        prefix = f"R10EK_{row['group']}"
        print(f"{prefix}_STATUS={row['status']}", flush=True)
        print(f"{prefix}_TRUST={row['trust']}", flush=True)
        print(f"{prefix}_COMPONENTS={row['components']}", flush=True)
        print(f"{prefix}_SUSPENSIONS={row['suspensions']}", flush=True)
        print(f"{prefix}_HIDDEN={row['hidden_inference_steps']}", flush=True)
        print(f"{prefix}_CONTRACT={row['shared_contract']}", flush=True)
    print(f"R10EK_REPORT={output / 'audit.json'}")
    print("R10EK_SHARED_DESIGN_AUDIT=PASS")
    print("R10EK_PRODUCTION_CHANGED=False")
    print("R10EK_FULL_PYTEST_RUN=False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
