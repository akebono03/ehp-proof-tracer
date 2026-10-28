"""Focused, read-only real-proof audit after the R10EL shared suppression patch."""
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
from phase169_r10el_shared_generator_suppression.core import (
    exclusive_generator_inference_indices,
)
from proof import ProofRule, Relation

CASES = (
    (22, 6, "cyclic", 14, 31),
    (22, 10, "cyclic", 10, 40),
    (15, 8, "direct_sum", 5, 10),
    (24, 9, "direct_sum", 13, 110),
)


def inspect_case(bridge: object, n: int, k: int,
                 shape: str, exponent: int, hidden_count: int,
                 output: Path) -> dict:
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    name = f"pi_{n+k}^{n}"
    if (result.status is not ProofSearchStatus.COMPLETE
            or result.open_goals or len(contexts) != 1):
        raise RuntimeError(f"R10EL incomplete proof: {name}")
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    derived = citing_id is None
    if derived and not (isinstance(result.conclusion, Relation)
                        and result.conclusion.lhs == result.target):
        raise RuntimeError(f"R10EL unscreened derived target: {name}")
    inferred, given = verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing_id,
        derived_target_without_citing_id=derived,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    order = tuple(item.step_index for item in project_narrative_order(model))
    before_steps = tuple(id(x) for x in model.steps)
    before_premises = tuple(tuple(id(p) for p in x.premises) for x in model.steps)
    display = (project_verified_stable_image_chain(model, order)
               if shape == "cyclic"
               else project_verified_direct_sum_transport(model, order))
    if display is None or len(display.hidden_indices) != hidden_count:
        raise RuntimeError(f"R10EL display regression: {name}")
    root = model.steps[model.root_index]
    _, _, *images = root.premises
    shared = exclusive_generator_inference_indices(
        model, order, images, model.root_index,
        require_all=shape == "direct_sum",
    )
    if shared is None or shared != display.hidden_indices:
        raise RuntimeError(f"R10EL shared contract mismatch: {name}")
    markdown = render_model_backed_narrative_markdown(result, model)
    metrics = count_rendered_image_equations(markdown)
    if (metrics["total_occurrences"] != 0
            or metrics["extra_duplicate_occurrences"] != 0
            or rf"E^{{{exponent}}}" not in markdown
            or not markdown.rstrip().endswith("□")):
        raise RuntimeError(f"R10EL narrative regression: {name}")
    for citation in model.citations:
        if f"**[R{citation.number}] " not in markdown:
            raise RuntimeError(f"R10EL lost Reference: {name}")
    if not set(display.citation_numbers).issubset({c.number for c in model.citations}):
        raise RuntimeError(f"R10EL unregistered citation: {name}")
    if (tuple(id(x) for x in model.steps) != before_steps
            or tuple(tuple(id(p) for p in x.premises) for x in model.steps) != before_premises
            or model.steps != result.proven_steps
            or any(model.steps[i].rule is not ProofRule.INFERENCE
                   or model.step_citation_numbers[i]
                   for i in display.hidden_indices)):
        raise RuntimeError(f"R10EL Proof Tree mutation or citation hiding: {name}")
    filename = f"pi_{n+k}_{n}.md"
    (output / filename).write_text(markdown, encoding="utf-8")
    return {
        "group": name, "shape": shape, "status": result.status.value,
        "trust": "PASS", "inference_steps": inferred, "given_steps": given,
        "proof_steps": len(result.proven_steps), "suspensions": exponent,
        "hidden_display_only": len(display.hidden_indices),
        "reference_count": len(model.citations),
        "duplicate_image_equations": metrics["extra_duplicate_occurrences"],
        "one_step_equations": metrics["total_occurrences"],
        "source_and_tree_preserved": True, "shared_contract": "PASS",
        "rendered_file": filename,
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m phase169_r10el_shared_generator_suppression.audit OUTPUT")
    output = Path(sys.argv[1]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    bridge = build_shared_typed_bridge()
    cases = [inspect_case(bridge, *case, output) for case in CASES]
    for case in cases:
        key = "R10EL_" + case["group"]
        print(key + "_STATUS=" + case["status"], flush=True)
        print(key + "_TRUST=" + case["trust"], flush=True)
        print(key + "_HIDDEN=" + str(case["hidden_display_only"]), flush=True)
        print(key + "_SHARED_CONTRACT=" + case["shared_contract"], flush=True)
        print(key + "_DUPLICATES=" + str(case["duplicate_image_equations"]), flush=True)
    report = {"phase": "169 R10EL", "mode": "TWO_PUBLIC_API_SHARED_SUPPRESSION",
              "proof_tree_changed": False, "inference_rules_changed": False,
              "full_pytest_run": False, "cases": cases}
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("R10EL_REPORT=" + str(output / "audit.json"), flush=True)
    print("R10EL_AUDIT_STATUS=PASS", flush=True)
    print("R10EL_FULL_PYTEST_RUN=False", flush=True)


if __name__ == "__main__":
    main()
