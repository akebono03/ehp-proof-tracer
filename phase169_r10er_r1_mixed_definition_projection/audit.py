"""R10ER live trust + mixed image compression, no new mathematical inference."""
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
from phase169_r10ec_direct_sum_narrative_projection.projection import (
    project_verified_direct_sum_transport,
)
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations,
)
from phase169_r10eq_r1_universal_stable_definition.definition import (
    expand_defined_stable_element_image,
)
from proof import ProofRule


CASES = (
    (30, 14, 14, (
        r"E^{14}(\sigma_{16}^{2})=\sigma_{30}^{2}",
        r"E^{14}(\kappa_{16})=\kappa_{30}",
    )),
    (30, 16, 12, (
        r"E^{12}(\omega_{18})=\omega_{30}",
        r"E^{12}(\sigma_{18}\mu_{25})=\sigma_{30}\mu_{37}",
    )),
    (30, 9, 19, (
        r"E^{19}(\nu_{11}^{3})=\nu_{30}^{3}",
        r"E^{19}(\mu_{11})=\mu_{30}",
    )),
)


def audit_case(bridge, n: int, k: int, exponent: int, formulae: tuple[str, ...], out: Path) -> dict:
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or result.open_goals or len(contexts) != 1:
        raise RuntimeError(f"incomplete search for pi_{n+k}^{n}")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    inferred, given = verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
        derived_target_without_citing_id=citing is None,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    order = tuple(row.step_index for row in project_narrative_order(model))
    original_steps = tuple(id(step) for step in model.steps)
    original_citations = model.step_citation_numbers
    display = project_verified_direct_sum_transport(model, order)
    if display is None or display.root_index != model.root_index:
        raise RuntimeError(f"missing certified display for pi_{n+k}^{n}")
    markdown = render_model_backed_narrative_markdown(result, model)
    if (display.statement not in markdown
            or not all(markdown.count(formula) == 1 for formula in formulae)
            or count_rendered_image_equations(markdown)["total_occurrences"] != 0
            or tuple(id(step) for step in model.steps) != original_steps
            or model.step_citation_numbers != original_citations
            or not markdown.rstrip().endswith("□")):
        raise RuntimeError(f"rendering/proof regression pi_{n+k}^{n}")
    definitions = sum(
        step.rule is ProofRule.INFERENCE and not step.premises
        and len(expand_defined_stable_element_image(step.conclusion)) == 1
        for step in model.steps
    )
    row = {
        "group": f"pi_{n+k}^{n}",
        "status": result.status.value,
        "trust": "PASS",
        "inference_steps": inferred,
        "given_steps": given,
        "definition_images": definitions,
        "exponent": exponent,
        "compressed_equations": len(formulae),
        "hidden_prose_only": len(display.hidden_indices),
        "individual_image_equations": 0,
        "citation_numbers": list(display.citation_numbers),
        "proof_tree_unchanged": True,
        "file": f"pi{n+k}_{n}.md",
    }
    (out / row["file"]).write_text(markdown, encoding="utf-8")
    return row


def main(argv=None) -> None:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        raise SystemExit("Usage: python -m phase169_r10er_r1_mixed_definition_projection.audit OUTPUT")
    out = Path(args[0]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    bridge = build_shared_typed_bridge()
    results = [audit_case(bridge, *case, out) for case in CASES]
    for row in results:
        prefix = "R10ER_" + row["group"]
        print(prefix + "_STATUS=" + row["status"], flush=True)
        print(prefix + "_TRUST=" + row["trust"], flush=True)
        print(prefix + "_DEFINITION_IMAGES=" + str(row["definition_images"]), flush=True)
        print(prefix + "_COMPRESSED_EQUATIONS=" + str(row["compressed_equations"]), flush=True)
        print(prefix + "_ONE_STEP_EQUATIONS=0", flush=True)
    report = {
        "phase": "169 R10ER-R1",
        "full_pytest_run": False,
        "production_changed": ["phase169_r10ec_direct_sum_narrative_projection/projection.py"],
        "new_inference_rules": 0,
        "new_cited_definitions": 0,
        "cases": results,
    }
    path = out / "audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("R10ER_AUDIT=" + str(path), flush=True)
    print("R10ER_LIVE_AUDIT=PASS", flush=True)


if __name__ == "__main__":
    main()
