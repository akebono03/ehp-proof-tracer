"""R10EN focused audit of unchanged citation provenance and complete proofs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import (
    resolve_specialized_goal_citing_id,
)
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
from phase169_r10em_citation_provenance_audit.provenance import (
    summarize_image_provenance,
    trace_generator_image_citations,
)
from phase169_r10en_shared_citation_provenance.core import (
    verified_generator_image_citation_numbers,
)
from proof import ProofRule, Relation

CASES = (
    (22, 6, "cyclic", 14, 31),
    (22, 10, "cyclic", 10, 40),
    (15, 8, "direct_sum", 5, 10),
    (24, 9, "direct_sum", 13, 110),
)


def inspect_case(
    bridge: object,
    n: int,
    k: int,
    shape: str,
    exponent: int,
    hidden_count: int,
    output: Path,
) -> dict:
    """Verify full proof first, then compare shared and diagnostic citations."""
    contexts: list[object] = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    name = f"pi_{n+k}^{n}"
    if (result.status is not ProofSearchStatus.COMPLETE
            or result.open_goals or len(contexts) != 1):
        raise RuntimeError("R10EN incomplete searched proof: " + name)
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing_id is None and not (
        isinstance(result.conclusion, Relation)
        and result.conclusion.lhs == result.target
    ):
        raise RuntimeError("R10EN target binding mismatch: " + name)
    inference_count, given_count = verify_proof_tree_for_narrative(
        result,
        contexts[0],
        citing_assertion_id=citing_id,
        derived_target_without_citing_id=citing_id is None,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    initial_ids = tuple(id(step) for step in model.steps)
    initial_edges = tuple(
        tuple(id(parent) for parent in step.premises) for step in model.steps
    )
    initial_citations = model.step_citation_numbers
    display = (
        project_verified_stable_image_chain(model, order)
        if shape == "cyclic" else project_verified_direct_sum_transport(model, order)
    )
    if display is None or len(display.hidden_indices) != hidden_count:
        raise RuntimeError("R10EN projection or hidden-index regression: " + name)
    root = model.steps[model.root_index]
    image_steps = root.premises[2:]
    numbers = verified_generator_image_citation_numbers(
        model, order, image_steps, require_each=shape == "direct_sum",
    )
    original = trace_generator_image_citations(model, order, image_steps)
    if numbers is None or original is None:
        raise RuntimeError("R10EN missing verified image provenance: " + name)
    summary = summarize_image_provenance(original, display.citation_numbers)
    if (numbers != display.citation_numbers
            or not summary["projection_matches_union"]
            or summary["missing_ancestors"]
            or summary["unregistered_citations"]
            or not summary["every_image_has_cited_given"]
            or summary["image_count"] != exponent * (
                1 if shape == "cyclic" else len(root.conclusion.rhs.summands)
            )):
        raise RuntimeError("R10EN citation-policy regression: " + name)
    markdown = render_model_backed_narrative_markdown(result, model)
    metrics = count_rendered_image_equations(markdown)
    if (metrics["total_occurrences"] != 0
            or metrics["extra_duplicate_occurrences"] != 0
            or rf"E^{{{exponent}}}" not in markdown
            or not markdown.rstrip().endswith("□")):
        raise RuntimeError("R10EN rendered narrative regression: " + name)
    if any(f"**[R{citation.number}] " not in markdown
           for citation in model.citations):
        raise RuntimeError("R10EN reference missing: " + name)
    if (tuple(id(step) for step in model.steps) != initial_ids
            or tuple(tuple(id(parent) for parent in step.premises)
                     for step in model.steps) != initial_edges
            or model.step_citation_numbers != initial_citations
            or model.steps != result.proven_steps
            or any(model.steps[index].rule is not ProofRule.INFERENCE
                   or model.step_citation_numbers[index]
                   for index in display.hidden_indices)):
        raise RuntimeError("R10EN unexpectedly modified Proof Tree: " + name)
    filename = f"pi_{n+k}_{n}.md"
    (output / filename).write_text(markdown, encoding="utf-8")
    return {
        "group": name,
        "shape": shape,
        "status": "complete",
        "trust": "PASS",
        "inference_steps": inference_count,
        "given_steps": given_count,
        "proof_step_count": len(model.steps),
        "image_count": len(image_steps),
        "images_with_cited_given": summary["images_with_cited_given"],
        "citations_match": True,
        "citation_numbers": list(numbers),
        "suspensions": exponent,
        "hidden_display_only": len(display.hidden_indices),
        "duplicate_image_prose": 0,
        "proof_tree_unchanged": True,
        "mathematical_inference_added": False,
        "rendered_file": filename,
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python -m phase169_r10en_shared_citation_provenance.audit OUTPUT_DIR"
        )
    output = Path(sys.argv[1]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    bridge = build_shared_typed_bridge()
    cases = [inspect_case(bridge, *case, output) for case in CASES]
    for case in cases:
        prefix = "R10EN_" + case["group"]
        for key, value in (
            ("STATUS", case["status"]),
            ("TRUST", case["trust"]),
            ("IMAGES", case["image_count"]),
            ("INDIVIDUALLY_CITED", case["images_with_cited_given"]),
            ("CITATIONS_MATCH", case["citations_match"]),
            ("HIDDEN", case["hidden_display_only"]),
            ("DUPLICATES", case["duplicate_image_prose"]),
        ):
            print(prefix + "_" + key + "=" + str(value), flush=True)
    report = {
        "phase": "169 R10EN",
        "mode": "FOCUSED_PRODUCTION_PATCH",
        "cases": cases,
        "inference_rules_changed": False,
        "proof_tree_changed": False,
        "full_pytest_run": False,
    }
    destination = output / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("R10EN_REPORT=" + str(destination), flush=True)
    print("R10EN_AUDIT_STATUS=PASS", flush=True)
    print("R10EN_FULL_PYTEST_RUN=False", flush=True)


if __name__ == "__main__":
    main()
